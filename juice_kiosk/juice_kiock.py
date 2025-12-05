import tkinter as tk
from tkinter import PhotoImage
from tkinter import messagebox
import os

# KioskApp 클래스는 주스 키오스크 GUI를 생성하고 이벤트를 처리합니다.
class KioskApp:
    def __init__(self, master):
        self.master = master
        master.title("주스 키오스크")
        # 윈도우 크기 변경 비활성화 (깔끔한 레이아웃 유지)
        master.resizable(False, False)

        # 초기 선택값 설정
        self.selected_fruit = "트리플 시트러스" 
        self.selected_size = "기본 컵" 
        
        # 8가지 최종 확정 메뉴의 가격 딕셔너리입니다. (코코넛, 패션프루트 제외)
        self.fruit_prices = {
            "트리플 시트러스": 5500,
            "클래식 그린 디톡스": 6300, 
            "루비 자몽 허니": 5000,
            "순수 망고 스무디": 6500, 
            "프리미엄 딸기": 5800,
            "민트 레모네이드": 4500,
            "베리 퍼플": 6200,
            "바나나 프로틴": 6000
        }

        # 컵 사이즈별 추가 요금을 저장하는 딕셔너리입니다.
        self.size_fees = {
            "기본 컵": 0,
            "중간 컵": 1000,
            "대": 2000
        }
        
        # 이미지 객체 참조 유지를 위한 리스트입니다.
        self.fruit_images = []
        self.size_images = []

        self.setup_gui()
        self.calculate_total_price()

    # GUI의 모든 위젯(Widget)을 설정하고 배치하는 메서드입니다.
    def setup_gui(self):
        
        # === 1. 과일 선택 섹션 ===
        tk.Label(self.master, text="과일을 선택하세요", font=('맑은 고딕', 18, 'bold')).pack(pady=10)
        
        # 8개의 버튼을 2x4 형태로 배치할 프레임입니다.
        self.fruit_frame = tk.Frame(self.master)
        self.fruit_frame.pack(padx=10, pady=5)
        
        # 8가지 최종 메뉴 정보와 JPG 이미지 파일 경로를 정의합니다.
        # 파일명은 assets 폴더의 이름과 일치해야 합니다. (image_f809a7.png 참조)
        fruit_info = [
            ("트리플 시트러스", "assets/citrus_mix.jpg"),
            ("클래식 그린 디톡스", "assets/green_detox.jpg"),
            ("루비 자몽 허니", "assets/grapefruit_honey.jpg"),
            ("순수 망고 스무디", "assets/mango_smoothie.jpg"),
            ("프리미엄 딸기", "assets/strawberry_premium.jpg"),
            ("민트 레모네이드", "assets/lemon_mint.jpg"),
            ("베리 퍼플", "assets/berry_purple.jpg"),
            ("바나나 프로틴", "assets/banana_protein.jpg")
        ]

        # 과일 버튼들을 생성하고 배치합니다.
        for idx, (name, path) in enumerate(fruit_info):
            # 2행 4열 그리드에 맞게 행(row)과 열(column)을 계산합니다.
            row_idx = idx // 4 # 0, 1, 2, 3 -> row 0 / 4, 5, 6, 7 -> row 1
            col_idx = idx % 4      

            if os.path.exists(path):
                # PhotoImage 객체를 생성하여 이미지를 로드합니다.
                try:
                    img = PhotoImage(file=path)
                    self.fruit_images.append(img)
                    
                    button = tk.Button(self.fruit_frame, image=img, text=name, compound='top', 
                                       font=('맑은 고딕', 12), width=120, height=180, 
                                       command=lambda fruit=name: self.fruit_select(fruit))
                    button.grid(row=row_idx, column=col_idx, padx=5, pady=5)
                except tk.TclError:
                    # JPG 파일이 너무 크거나 Tkinter가 지원하지 않는 포맷일 경우 처리 (Tkinter는 JPG 지원이 제한적입니다.)
                    print(f"오류: {path} 파일 로드 실패. PNG 또는 GIF로 변환을 권장합니다.")
                    self._create_text_button(name, row_idx, col_idx, is_fruit=True)
            else:
                # 이미지 파일이 없을 경우 텍스트 버튼으로 대체합니다.
                print(f"경고: 이미지 파일을 찾을 수 없습니다: {path}")
                self._create_text_button(name, row_idx, col_idx, is_fruit=True)
        
        # === 2. 컵 사이즈 선택 섹션 ===
        tk.Label(self.master, text="컵 사이즈를 선택하세요", font=('맑은 고딕', 18, 'bold')).pack(pady=10)
        self.size_frame = tk.Frame(self.master)
        self.size_frame.pack(padx=10, pady=5)

        # 컵 사이즈 정보와 JPG 이미지 파일 경로를 정의합니다.
        # 파일명은 assets 폴더의 이름과 일치해야 합니다. (image_f809a7.png 참조)
        size_info = [
            ("기본 컵", "assets/small.jpg"),
            ("중간 컵", "assets/medium.jpg"),
            ("대", "assets/large.jpg")
        ]
        
        # 컵 사이즈 버튼들을 생성하고 배치합니다.
        for idx, (name, path) in enumerate(size_info):
            if os.path.exists(path):
                try:
                    img = PhotoImage(file=path)
                    self.size_images.append(img)
                    
                    button = tk.Button(self.size_frame, image=img, text=name, compound='top', 
                                       font=('맑은 고딕', 12), width=120, height=180, 
                                       command=lambda size=name: self.size_select(size))
                    button.grid(row=0, column=idx, padx=5, pady=5)
                except tk.TclError:
                    print(f"오류: {path} 파일 로드 실패. PNG 또는 GIF로 변환을 권장합니다.")
                    self._create_text_button(name, 0, idx, is_fruit=False)
            else:
                print(f"경고: 이미지 파일을 찾을 수 없습니다: {path}")
                self._create_text_button(name, 0, idx, is_fruit=False)

        # === 3. 결과 표시 섹션 ===
        self.result_text = tk.StringVar()
        self.total_price_label = tk.Label(self.master, textvariable=self.result_text, 
                                          font=('맑은 고딕', 16, 'bold'), fg='blue')
        self.total_price_label.pack(pady=20)

    # 이미지 로드 실패 시 대체 텍스트 버튼을 생성하는 내부 메서드입니다.
    def _create_text_button(self, name, row_idx, col_idx, is_fruit):
        if is_fruit:
            text_content = name + f"\n({self.fruit_prices[name]:,}원)"
            frame = self.fruit_frame
            command_func = lambda fruit=name: self.fruit_select(fruit)
        else:
            text_content = name
            frame = self.size_frame
            command_func = lambda size=name: self.size_select(size)
            
        tk.Button(frame, text=text_content, font=('맑은 고딕', 12), width=15, height=5,
                          command=command_func).grid(row=row_idx, column=col_idx, padx=5, pady=5)


    # 과일 선택 시 호출되는 메서드입니다.
    def fruit_select(self, fruit_name):
        self.selected_fruit = fruit_name
        self.calculate_total_price()

    # 컵 사이즈 선택 시 호출되는 메서드입니다.
    def size_select(self, size_name):
        self.selected_size = size_name
        self.calculate_total_price()

    # 총 금액을 계산하고 화면에 표시하는 메서드입니다.
    def calculate_total_price(self):
        try:
            fruit_base_price = self.fruit_prices.get(self.selected_fruit, 0)
            size_extra_fee = self.size_fees.get(self.selected_size, 0)
            
            total_amount = fruit_base_price + size_extra_fee

            # 표시할 문자열 포맷팅
            display_text = (
                f"선택: {self.selected_fruit} / {self.selected_size}\n"
                f"총 금액: {total_amount:,}원"
            )
            
            self.result_text.set(display_text)

        except Exception as e:
            self.result_text.set("오류 발생: 가격 계산 불가")
            messagebox.showerror("가격 오류", f"가격 계산 중 오류가 발생했습니다: {e}")


# 메인 함수: 프로그램의 진입점입니다.
if __name__ == '__main__':
    # Tkinter는 JPG 지원에 제한이 있거나 Tcl/Tk 버전에 따라 실패할 수 있습니다.
    # 만약 실행이 안 된다면 이미지들을 PNG 또는 GIF로 변환해 보시옵소서.
    root = tk.Tk()
    app = KioskApp(root)
    root.mainloop()
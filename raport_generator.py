import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import pandas as pd
from fpdf import FPDF
import random
from datetime import datetime
import os


class PDFReport(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 15)
       
        self.cell(0, 10, 'Raport Analityczny Sprzedazy', 0, 1, 'C')
        self.ln(5)
        
    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Strona {self.page_no()}', 0, 0, 'C')

    def chapter_title(self, title):
        self.set_font('Arial', 'B', 12)
        self.set_fill_color(200, 220, 255)
       
        self.cell(0, 10, title, 0, 1, 'L', 1)
        self.ln(4)

    def chapter_body(self, body):
        self.set_font('Arial', '', 11)
        self.multi_cell(0, 10, body)
        self.ln()

    def add_table(self, dataframe):
        self.set_font('Arial', 'B', 10)
     
        for col in dataframe.columns:
            
            text = str(col).encode('latin-1', 'replace').decode('latin-1')
            self.cell(45, 10, text, 1, 0, 'C')
        self.ln()
        
       
        self.set_font('Arial', '', 10)
        for i in range(len(dataframe)):
            row = dataframe.iloc[i]
            for col in dataframe.columns:
                text = str(row[col]).encode('latin-1', 'replace').decode('latin-1')
                self.cell(45, 10, text, 1, 0, 'C')
            self.ln()


class ReportApp:
    def __init__(self, root):
        self.root = root
        self.root.title("System Generowania Raportow PDF v1.0")
        self.root.geometry("600x450")
        
        style = ttk.Style()
        style.theme_use('clam')
        
        
        frame_data = ttk.LabelFrame(root, text=" 1. Zrodlo Danych ", padding=20)
        frame_data.pack(pady=20, padx=20, fill="x")
        
        self.lbl_status = ttk.Label(frame_data, text="Status: Brak danych. Wygeneruj losowe lub wczytaj CSV.")
        self.lbl_status.pack(pady=5)
        
        btn_frame = ttk.Frame(frame_data)
        btn_frame.pack(fill="x", pady=5)
        
        ttk.Button(btn_frame, text="Generuj Losowe Dane", command=self.generate_dummy_data).pack(side="left", padx=5, expand=True)
        ttk.Button(btn_frame, text="Wczytaj CSV", command=self.load_csv).pack(side="left", padx=5, expand=True)

        
        frame_preview = ttk.LabelFrame(root, text=" 2. Podglad Danych (Ostatnie 5 rekordow) ", padding=20)
        frame_preview.pack(pady=10, padx=20, fill="both", expand=True)
        
       
        self.tree = ttk.Treeview(frame_preview, columns=('Produkt', 'Ilosc', 'Cena', 'Suma'), show='headings', height=5)
        self.tree.heading('Produkt', text='Produkt')
        self.tree.heading('Ilosc', text='Ilosc') # Zmiana: Ilość -> Ilosc
        self.tree.heading('Cena', text='Cena (PLN)')
        self.tree.heading('Suma', text='Suma (PLN)')
        
        for col in ('Produkt', 'Ilosc', 'Cena', 'Suma'):
            self.tree.column(col, width=100, anchor='center')
            
        self.tree.pack(fill="both", expand=True)

      
        ttk.Button(root, text="GENERUJ RAPORT PDF", command=self.generate_pdf).pack(pady=20, ipadx=20, ipady=10)

        self.df = None

    def generate_dummy_data(self):
        products = ['Laptop', 'Myszka', 'Klawiatura', 'Monitor', 'Sluchawki', 'Kabel HDMI'] # Sluchawki bez ł
        data = []
        for _ in range(15):
            prod = random.choice(products)
            qty = random.randint(1, 10)
            price = random.randint(50, 3000)
            data.append([prod, qty, price, qty*price])
        
        
        self.df = pd.DataFrame(data, columns=['Produkt', 'Ilosc', 'Cena', 'Suma'])
        self.update_preview()
        self.lbl_status.config(text="Status: Wygenerowano dane testowe.", foreground="green")

    def load_csv(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if file_path:
            try:
                self.df = pd.read_csv(file_path)
              
                self.df.columns = [c.replace('ł', 'l').replace('ś', 's').replace('ż', 'z') for c in self.df.columns]
                self.update_preview()
                self.lbl_status.config(text=f"Status: Wczytano {os.path.basename(file_path)}", foreground="green")
            except Exception as e:
                messagebox.showerror("Blad", f"Nie udalo sie wczytac pliku:\n{e}")

    def update_preview(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        
        if self.df is not None:
            for index, row in self.df.tail(5).iterrows():
                self.tree.insert("", "end", values=list(row))

    def generate_pdf(self):
        if self.df is None:
            messagebox.showwarning("Uwaga", "Najpierw wczytaj lub wygeneruj dane!")
            return

        try:
            pdf = PDFReport()
            pdf.add_page()
            
            total_sales = self.df['Suma'].sum()
            
            best_product = self.df.groupby('Produkt')['Ilosc'].sum().idxmax()
            
           
            pdf.chapter_title(f"Podsumowanie - {datetime.now().strftime('%Y-%m-%d')}")
            pdf.chapter_body(
                f"Calkowita wartosc sprzedazy: {total_sales} PLN.\n"
                f"Najlepiej sprzedajacy sie produkt: {best_product}.\n"
                f"Liczba przetworzonych transakcji: {len(self.df)}."
            )
            
            pdf.chapter_title("Szczegoly Transakcji (Top 10)")
            top_df = self.df.head(10)
            pdf.add_table(top_df)
            
            filename = f"Raport_Sprzedazy_{datetime.now().strftime('%H%M%S')}.pdf"
            pdf.output(filename)
            
            messagebox.showinfo("Sukces", f"Raport wygenerowany:\n{filename}")
            os.system(f"start {filename}")
            
        except Exception as e:
            messagebox.showerror("Blad krytyczny", f"Nie udalo sie wygenerowac PDF:\n{e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ReportApp(root)

    root.mainloop()

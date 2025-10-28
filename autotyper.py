"""
AutoTyper v4.0 - SOLUÇÃO DEFINITIVA
Usa pynput para digitação perfeita com acentos
"""

import time
import tkinter as tk
from tkinter import scrolledtext, messagebox, ttk
import threading
from pynput.keyboard import Controller, Key

class AutoTyperApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AutoTyper v4.0 - Solução Definitiva")
        self.root.geometry("750x650")
        self.root.resizable(True, True)
        
        # Variáveis
        self.is_typing = False
        self.typing_thread = None
        self.keyboard = Controller()
        
        # Configuração da interface
        self.setup_ui()
        
    def setup_ui(self):
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(3, weight=1)
        
        # Título
        title_label = ttk.Label(main_frame, text="⚡ AutoTyper v4.0 - Acentos Perfeitos!", 
                                font=('Arial', 18, 'bold'))
        title_label.grid(row=0, column=0, pady=(0, 5))
        
        # Subtítulo
        subtitle_label = ttk.Label(main_frame, 
                                text="✅ 100% funcional com acentos | ✅ Digita caractere real | ✅ Sem Ctrl+V", 
                                font=('Arial', 9, 'italic'), foreground='green')
        subtitle_label.grid(row=1, column=0, pady=(0, 10))
        
        # Frame de instruções
        instructions_frame = ttk.LabelFrame(main_frame, text="📋 Instruções - LEIA COM ATENÇÃO!", padding="10")
        instructions_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        instructions = """1. Cole seu texto completo na área abaixo
2. Configure a velocidade (10-20ms = ultra rápido | 30-50ms = recomendado | 60-100ms = seguro)
3. Clique em "Iniciar Digitação"
4. Você terá 5 segundos para clicar no campo da Redação Paraná
5. NÃO TOQUE em nada durante a digitação!

✅ AGORA SIM: Acentos funcionam 100% (ã, é, í, ó, ú, â, ê, ô, à, ç)
⚠️ IMPORTANTE: Mantenha esta janela minimizada após iniciar (não feche!)"""
        
        instructions_label = ttk.Label(instructions_frame, text=instructions, 
                                       justify=tk.LEFT, wraplength=700)
        instructions_label.grid(row=0, column=0)
        
        # Área de texto
        text_frame = ttk.LabelFrame(main_frame, text="✍️ Seu Texto (com acentos!)", padding="10")
        text_frame.grid(row=3, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        text_frame.columnconfigure(0, weight=1)
        text_frame.rowconfigure(0, weight=1)
        
        self.text_area = scrolledtext.ScrolledText(text_frame, wrap=tk.WORD, 
                                                   width=80, height=10,
                                                   font=('Arial', 11))
        self.text_area.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Contador
        self.char_count_var = tk.StringVar(value="0 caracteres")
        char_count_label = ttk.Label(text_frame, textvariable=self.char_count_var,
                                     font=('Arial', 9), foreground='#666')
        char_count_label.grid(row=1, column=0, sticky=tk.E, pady=(5, 0))
        
        self.text_area.bind('<KeyRelease>', self.update_char_count)
        
        # Frame de controles
        controls_frame = ttk.LabelFrame(main_frame, text="⚙️ Configurações", padding="10")
        controls_frame.grid(row=4, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Velocidade
        speed_label = ttk.Label(controls_frame, text="⚡ Velocidade (milissegundos):")
        speed_label.grid(row=0, column=0, padx=(0, 10), sticky=tk.W)
        
        self.speed_var = tk.StringVar(value="30")
        speed_spinbox = ttk.Spinbox(controls_frame, from_=10, to=200, 
                                    textvariable=self.speed_var, width=10)
        speed_spinbox.grid(row=0, column=1, padx=(0, 20))
        
        # Presets
        preset_frame = ttk.Frame(controls_frame)
        preset_frame.grid(row=0, column=2, columnspan=3)
        
        ttk.Button(preset_frame, text="🚀 Ultra (15ms)", 
                  command=lambda: self.speed_var.set("15"), width=14).pack(side=tk.LEFT, padx=2)
        ttk.Button(preset_frame, text="⚡ Rápido (30ms)", 
                  command=lambda: self.speed_var.set("30"), width=14).pack(side=tk.LEFT, padx=2)
        ttk.Button(preset_frame, text="✅ Seguro (50ms)", 
                  command=lambda: self.speed_var.set("50"), width=14).pack(side=tk.LEFT, padx=2)
        ttk.Button(preset_frame, text="🐢 Humano (80ms)", 
                  command=lambda: self.speed_var.set("80"), width=14).pack(side=tk.LEFT, padx=2)
        
        # Delay
        delay_label = ttk.Label(controls_frame, text="⏱️ Tempo para clicar no campo:")
        delay_label.grid(row=1, column=0, padx=(0, 10), sticky=tk.W, pady=(10, 0))
        
        self.delay_var = tk.StringVar(value="5")
        delay_spinbox = ttk.Spinbox(controls_frame, from_=3, to=10, 
                                    textvariable=self.delay_var, width=10)
        delay_spinbox.grid(row=1, column=1, pady=(10, 0))
        
        # Estimativa
        self.time_estimate_var = tk.StringVar(value="")
        time_estimate_label = ttk.Label(controls_frame, textvariable=self.time_estimate_var,
                                       font=('Arial', 9, 'italic'), foreground='blue')
        time_estimate_label.grid(row=1, column=2, columnspan=3, pady=(10, 0), padx=(20, 0))
        
        # Botões
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=5, column=0, pady=(0, 10))
        
        self.start_button = ttk.Button(button_frame, text="🚀 Iniciar Digitação", 
                                       command=self.start_typing, width=25)
        self.start_button.grid(row=0, column=0, padx=5)
        
        self.stop_button = ttk.Button(button_frame, text="⏹️ Parar Agora", 
                                      command=self.stop_typing, width=18, state='disabled')
        self.stop_button.grid(row=0, column=1, padx=5)
        
        clear_button = ttk.Button(button_frame, text="🗑️ Limpar", 
                                 command=self.clear_text, width=18)
        clear_button.grid(row=0, column=2, padx=5)
        
        # Progresso
        progress_frame = ttk.Frame(main_frame)
        progress_frame.grid(row=6, column=0, sticky=(tk.W, tk.E))
        progress_frame.columnconfigure(0, weight=1)
        
        self.progress_bar = ttk.Progressbar(progress_frame, length=400, mode='determinate')
        self.progress_bar.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 5))
        
        self.progress_var = tk.StringVar(value="✅ Pronto para digitar")
        progress_label = ttk.Label(progress_frame, textvariable=self.progress_var, 
                                   font=('Arial', 11, 'bold'))
        progress_label.grid(row=1, column=0)
    
    def update_char_count(self, event=None):
        text = self.text_area.get("1.0", tk.END).strip()
        char_count = len(text)
        word_count = len(text.split()) if text else 0
        self.char_count_var.set(f"{char_count} caracteres | {word_count} palavras")
        
        if char_count > 0:
            try:
                speed_ms = int(self.speed_var.get())
                total_seconds = (char_count * speed_ms) / 1000
                minutes = int(total_seconds // 60)
                seconds = int(total_seconds % 60)
                self.time_estimate_var.set(f"⏱️ Tempo: ~{minutes}min {seconds}s")
            except:
                self.time_estimate_var.set("")
        else:
            self.time_estimate_var.set("")
    
    def start_typing(self):
        text = self.text_area.get("1.0", tk.END).strip()
        
        if not text:
            messagebox.showwarning("Aviso", "Digite ou cole o texto primeiro!")
            return
        
        try:
            speed = int(self.speed_var.get()) / 1000
            delay = int(self.delay_var.get())
        except ValueError:
            messagebox.showerror("Erro", "Valores inválidos!")
            return
        
        # Confirmar
        result = messagebox.askyesno("Confirmar", 
            f"Digitar {len(text)} caracteres?\n\n"
            f"Você terá {delay} segundos para clicar no campo.\n\n"
            f"Tempo estimado: ~{int(len(text) * speed)}s\n\n"
            "Pronto para começar?")
        
        if not result:
            return
        
        self.is_typing = True
        self.start_button.config(state='disabled')
        self.stop_button.config(state='normal')
        self.text_area.config(state='disabled')
        self.progress_bar['value'] = 0
        
        self.typing_thread = threading.Thread(target=self.type_text, 
                                              args=(text, speed, delay))
        self.typing_thread.daemon = True
        self.typing_thread.start()
    
    def type_text(self, text, speed, delay):
        try:
            # Countdown
            for i in range(delay, 0, -1):
                if not self.is_typing:
                    return
                self.progress_var.set(f"⏳ CLIQUE NO CAMPO AGORA! {i}...")
                time.sleep(1)
            
            self.progress_var.set("✍️ Digitando... NÃO MEXA!")
            total_chars = len(text)
            
            # Digitar cada caractere
            for idx, char in enumerate(text):
                if not self.is_typing:
                    self.progress_var.set("❌ Parado pelo usuário")
                    break
                
                # Digitar usando pynput (funciona com acentos!)
                try:
                    self.keyboard.type(char)
                except:
                    # Fallback para caracteres especiais
                    if char == '\n':
                        self.keyboard.press(Key.enter)
                        self.keyboard.release(Key.enter)
                    elif char == '\t':
                        self.keyboard.press(Key.tab)
                        self.keyboard.release(Key.tab)
                    else:
                        self.keyboard.type(char)
                
                time.sleep(speed)
                
                # Atualizar progresso
                if idx % 10 == 0:
                    progress = int(((idx + 1) / total_chars) * 100)
                    self.progress_bar['value'] = progress
                    self.progress_var.set(f"✍️ {progress}% ({idx + 1}/{total_chars})")
            
            if self.is_typing:
                self.progress_bar['value'] = 100
                self.progress_var.set("✅ CONCLUÍDO COM SUCESSO!")
                
                # Tocar beep de conclusão (opcional)
                try:
                    import winsound
                    winsound.Beep(1000, 200)
                except:
                    pass
                
                messagebox.showinfo("Sucesso! 🎉", 
                    f"Texto digitado com perfeição!\n\n"
                    f"✅ {total_chars} caracteres\n"
                    f"⏱️ Tempo: ~{int(total_chars * speed)}s\n\n"
                    "Verifique o texto na plataforma!")
        
        except Exception as e:
            self.progress_var.set(f"❌ ERRO: {str(e)}")
            messagebox.showerror("Erro", f"Erro ao digitar:\n{str(e)}")
        
        finally:
            self.is_typing = False
            self.start_button.config(state='normal')
            self.stop_button.config(state='disabled')
            self.text_area.config(state='normal')
    
    def stop_typing(self):
        self.is_typing = False
        self.progress_var.set("⏹️ PARADO pelo usuário")
    
    def clear_text(self):
        self.text_area.delete("1.0", tk.END)
        self.char_count_var.set("0 caracteres | 0 palavras")
        self.time_estimate_var.set("")
        self.progress_var.set("✅ Pronto para digitar")
        self.progress_bar['value'] = 0


def main():
    root = tk.Tk()
    app = AutoTyperApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
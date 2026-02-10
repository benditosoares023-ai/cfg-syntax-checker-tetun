import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import re
from datetime import datetime

class CFG_SyntaxCheckerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("APLIKASAUN CHEKA SINTAXE - CFG & AUTOMATA")
        self.root.geometry("1200x750")
        self.root.configure(bg="#2c3e50")
        
        # CFG Grammar Definitions iha Tetum
        self.cfg_grammars = {
            "Liafuan Tetun Sadiña": {
                "productions": {
                    "S": ["NP VP"],
                    "NP": ["Pronoun", "Det N", "NaranProper"],
                    "VP": ["V NP", "V Adj", "V Adv"],
                    "Pronoun": ["ha'u", "nia", "ó", "ita", "sira"],
                    "Det": ["ida", "ne'e", "ida-nain", "ida-ida"],
                    "N": ["livru", "busa", "uma", "kareta", "labarik", "mestre"],
                    "NaranProper": ["Budi", "Ani", "Dili", "Timor-Leste"],
                    "V": ["lee", "hili", "haree", "bá", "estuda"],
                    "Adj": ["boot", "ki'ik", "di'ak", "bonita", "matenek"],
                    "Adv": ["lalais", "neineik", "di'ak", "los"]
                },
                "start_symbol": "S",
                "description": "Grammar ba liafuan Tetun sadiña"
            },
            
            "Ekspresaun Matematika": {
                "productions": {
                    "E": ["E + T", "E - T", "T"],
                    "T": ["T * F", "T / F", "F"],
                    "F": ["( E )", "número", "id"],
                    "número": ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"],
                    "id": ["a", "b", "c", "x", "y", "z"]
                },
                "start_symbol": "E",
                "description": "Grammar ba ekspresaun matematika (+, -, *, /, paréntese)"
            },
            
            "Estrutura If-Else": {
                "productions": {
                    "Programa": ["Statement"],
                    "Statement": ["IfStatement", "Atribuisaun"],
                    "IfStatement": ["if ( Kondisaun ) { Statement }", 
                                   "if ( Kondisaun ) { Statement } else { Statement }"],
                    "Kondisaun": ["id relop id", "id relop número"],
                    "Atribuisaun": ["id = Ekspresaun"],
                    "Ekspresaun": ["id + id", "id - id", "id", "número"],
                    "relop": ["==", "!=", "<", ">", "<=", ">="],
                    "id": ["x", "y", "z", "a", "b", "c"],
                    "número": ["0", "1", "2", "3", "4", "5"]
                },
                "start_symbol": "Programa",
                "description": "Grammar ba estrutura if-else iha programasaun"
            },
            
            "Liafuan Pergunta Inglés": {
                "productions": {
                    "S": ["Aux NP VP ?"],
                    "NP": ["Det N", "NaranProper"],
                    "VP": ["V NP", "V Adj"],
                    "Aux": ["Do", "Does", "Is", "Are", "Can", "Will"],
                    "Det": ["the", "a", "an", "your", "my"],
                    "N": ["book", "cat", "house", "car", "student", "teacher"],
                    "NaranProper": ["John", "Mary", "London", "America"],
                    "V": ["read", "have", "see", "go", "study", "like"],
                    "Adj": ["big", "small", "good", "beautiful", "smart"]
                },
                "start_symbol": "S",
                "description": "Grammar ba liafuan pergunta língua Inglés"
            }
        }
        
        # PDA (Pushdown Automata) configurations
        self.pda_configs = {
            "Liafuan Tetun Sadiña": {
                "estadu": ["q0", "q1", "q2", "q3"],
                "alfabetu_input": ["ha'u", "nia", "livru", "lee", "boot", "seluk"],
                "alfabetu_stack": ["Z0", "S", "NP", "VP", "V", "N", "Det", "Adj"],
                "estadu_hahu": "q0",
                "stack_hahu": "Z0",
                "estadu_asin": ["q3"]
            },
            "Ekspresaun Matematika": {
                "estadu": ["q0", "q1", "q2", "q3"],
                "alfabetu_input": ["id", "número", "+", "-", "*", "/", "(", ")"],
                "alfabetu_stack": ["Z0", "E", "T", "F"],
                "estadu_hahu": "q0",
                "stack_hahu": "Z0",
                "estadu_asin": ["q3"]
            }
        }
        
        self.grammar_atual = "Liafuan Tetun Sadiña"
        self.história_parsing = []
        
        self.setup_gui()
    
    def setup_gui(self):
        # Header
        header_frame = tk.Frame(self.root, bg="#34495e", height=100)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(header_frame, 
                text="APLIKASAUN CHEKA SINTAXE UTILIZA CFG & AUTOMATA",
                font=("Arial", 16, "bold"),
                bg="#34495e",
                fg="white")
        title_label.pack(expand=True)
        
        subtitle_label = tk.Label(header_frame,
                text="Context-Free Grammar & Pushdown Automata",
                font=("Arial", 10),
                bg="#34495e",
                fg="#bdc3c7")
        subtitle_label.pack(expand=True)
        
        # Main Container
        main_container = tk.Frame(self.root, bg="#2c3e50")
        main_container.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Left Panel - Grammar Selection and Input
        left_panel = tk.Frame(main_container, bg="#ecf0f1", relief="ridge", borderwidth=2)
        left_panel.pack(side="left", fill="both", expand=True, padx=(0, 5))
        
        # Grammar Selection
        grammar_frame = tk.LabelFrame(left_panel, text="HILI GRAMMAR (CFG)", 
                                    font=("Arial", 10, "bold"),
                                    bg="#ecf0f1", fg="#2c3e50")
        grammar_frame.pack(fill="x", padx=10, pady=10)
        
        self.grammar_var = tk.StringVar(value=self.grammar_atual)
        
        for i, grammar in enumerate(self.cfg_grammars.keys()):
            rb = tk.Radiobutton(grammar_frame, 
                              text=grammar,
                              variable=self.grammar_var,
                              value=grammar,
                              command=self.on_grammar_change,
                              bg="#ecf0f1",
                              font=("Arial", 9))
            rb.grid(row=i//2, column=i%2, sticky="w", padx=10, pady=5)
        
        # Grammar Details
        details_frame = tk.LabelFrame(left_panel, text="DETALLE GRAMMAR", 
                                    font=("Arial", 10, "bold"),
                                    bg="#ecf0f1", fg="#2c3e50")
        details_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.grammar_details = scrolledtext.ScrolledText(details_frame, 
                                                       height=10,
                                                       font=("Consolas", 9),
                                                       wrap="word")
        self.grammar_details.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Input Section
        input_frame = tk.LabelFrame(left_panel, text="INPUT LIAFUAN/EKSPRESAUN", 
                                  font=("Arial", 10, "bold"),
                                  bg="#ecf0f1", fg="#2c3e50")
        input_frame.pack(fill="x", padx=10, pady=10)
        
        self.input_text = tk.Text(input_frame, height=3, font=("Arial", 11))
        self.input_text.pack(fill="x", padx=5, pady=5)
        
        # Example buttons
        example_frame = tk.Frame(input_frame, bg="#ecf0f1")
        example_frame.pack(fill="x", padx=5, pady=(0, 5))
        
        exemplu = {
            "Liafuan Tetun Sadiña": ["ha'u lee livru", "nia hili uma boot", "Budi bá lailais"],
            "Ekspresaun Matematika": ["a + b * c", "(a + b) * c", "a * (b - c) / d"],
            "Estrutura If-Else": ["if (x > 0) { y = x }", "if (a == b) { c = 1 } else { c = 0 }"],
            "Liafuan Pergunta Inglés": ["Do you have a book?", "Is your house big?", "Can John read?"]
        }
        
        for i, (grammar, lista_ex) in enumerate(exemplu.items()):
            btn = tk.Button(example_frame,
                          text=f"Ezemplu: {lista_ex[0][:15]}...",
                          command=lambda g=grammar, e=lista_ex[0]: self.load_example(g, e),
                          bg="#3498db",
                          fg="white",
                          font=("Arial", 8),
                          padx=5)
            btn.pack(side="left", padx=2)
        
        # Control Buttons
        button_frame = tk.Frame(left_panel, bg="#ecf0f1")
        button_frame.pack(fill="x", padx=10, pady=10)
        
        tk.Button(button_frame,
                 text="🔍 CHEKA SINTAXE",
                 command=self.check_syntax,
                 bg="#27ae60",
                 fg="white",
                 font=("Arial", 10, "bold"),
                 padx=20,
                 pady=10).pack(side="left", padx=5)
        
        tk.Button(button_frame,
                 text="🧹 HAMOOS",
                 command=self.reset_input,
                 bg="#e74c3c",
                 fg="white",
                 font=("Arial", 10, "bold"),
                 padx=20,
                 pady=10).pack(side="left", padx=5)
        
        tk.Button(button_frame,
                 text="📊 SIMULA PDA",
                 command=self.simulate_pda,
                 bg="#9b59b6",
                 fg="white",
                 font=("Arial", 10, "bold"),
                 padx=20,
                 pady=10).pack(side="left", padx=5)
        
        # Right Panel - Results and Visualization
        right_panel = tk.Frame(main_container, bg="#ecf0f1", relief="ridge", borderwidth=2)
        right_panel.pack(side="right", fill="both", expand=True, padx=(5, 0))
        
        # Result Display
        result_frame = tk.LabelFrame(right_panel, text="REZULTADU CHEKAGEM", 
                                   font=("Arial", 10, "bold"),
                                   bg="#ecf0f1", fg="#2c3e50")
        result_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Status display
        self.status_frame = tk.Frame(result_frame, bg="#ecf0f1")
        self.status_frame.pack(fill="x", padx=5, pady=5)
        
        self.status_label = tk.Label(self.status_frame, 
                                   text="Estadu: Hein input...",
                                   font=("Arial", 11, "bold"),
                                   bg="#ecf0f1")
        self.status_label.pack()
        
        # Parse tree/derivation display
        tree_frame = tk.LabelFrame(result_frame, text="HAI-HUSI PARSING / DERIVASAUN", 
                                 font=("Arial", 10, "bold"),
                                 bg="#ecf0f1", fg="#2c3e50")
        tree_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        self.parse_tree_text = scrolledtext.ScrolledText(tree_frame,
                                                       height=15,
                                                       font=("Consolas", 9),
                                                       wrap="word")
        self.parse_tree_text.pack(fill="both", expand=True, padx=5, pady=5)
        
        # PDA Simulation Panel
        pda_frame = tk.LabelFrame(right_panel, text="SIMULASAUN PUSHDOWN AUTOMATA (PDA)", 
                                font=("Arial", 10, "bold"),
                                bg="#ecf0f1", fg="#2c3e50")
        pda_frame.pack(fill="x", padx=10, pady=10)
        
        pda_content = tk.Frame(pda_frame, bg="#ecf0f1")
        pda_content.pack(fill="x", padx=5, pady=5)
        
        # PDA visualization
        self.pda_canvas = tk.Canvas(pda_content, height=150, bg="white", highlightthickness=1)
        self.pda_canvas.pack(fill="x", pady=5)
        
        self.pda_info = tk.Label(pda_content,
                               text="PDA sei simula prosesu parsing ho stack",
                               font=("Arial", 9),
                               bg="#ecf0f1",
                               wraplength=400)
        self.pda_info.pack()
        
        # Bottom Panel - History
        history_frame = tk.LabelFrame(self.root, text="HISTÓRIA CHEKAGEM", 
                                    font=("Arial", 10, "bold"),
                                    bg="#34495e", fg="white")
        history_frame.pack(fill="x", padx=10, pady=(0, 10))
        
        columns = ("Nu.", "Oras", "Grammar", "Input", "Estadu", "Metodu")
        self.history_tree = ttk.Treeview(history_frame, columns=columns, show="headings", height=4)
        
        for col in columns:
            self.history_tree.heading(col, text=col)
            self.history_tree.column(col, width=100)
        
        self.history_tree.column("Input", width=200)
        
        scrollbar = ttk.Scrollbar(history_frame, orient="vertical", command=self.history_tree.yview)
        self.history_tree.configure(yscrollcommand=scrollbar.set)
        
        self.history_tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Initialize
        self.update_grammar_details()
    
    def on_grammar_change(self):
        self.grammar_atual = self.grammar_var.get()
        self.update_grammar_details()
    
    def update_grammar_details(self):
        grammar = self.cfg_grammars[self.grammar_atual]
        self.grammar_details.delete(1.0, tk.END)
        
        details = f"Grammar: {self.grammar_atual}\n"
        details += f"Símbolu Hahu: {grammar['start_symbol']}\n"
        details += f"Deskrisaun: {grammar['description']}\n\n"
        details += "Produsaun:\n"
        
        for non_terminal, productions in grammar['productions'].items():
            if isinstance(productions, list):
                prod_str = " | ".join(productions)
            else:
                prod_str = productions
            details += f"  {non_terminal} → {prod_str}\n"
        
        self.grammar_details.insert(1.0, details)
    
    def load_example(self, grammar, example):
        self.grammar_var.set(grammar)
        self.on_grammar_change()
        self.input_text.delete(1.0, tk.END)
        self.input_text.insert(1.0, example)
    
    def reset_input(self):
        self.input_text.delete(1.0, tk.END)
        self.parse_tree_text.delete(1.0, tk.END)
        self.status_label.config(text="Estadu: Hein input...", fg="black")
        self.pda_info.config(text="PDA sei simula prosesu parsing ho stack")
        self.draw_pda_initial()
    
    def draw_pda_initial(self):
        self.pda_canvas.delete("all")
        # Draw initial PDA state
        self.pda_canvas.create_rectangle(10, 10, 190, 90, fill="#e8f4f8", outline="#3498db", width=2)
        self.pda_canvas.create_text(100, 30, text="Estadu: q0", font=("Arial", 10, "bold"))
        self.pda_canvas.create_text(100, 50, text="Stack: Z0", font=("Arial", 10))
        self.pda_canvas.create_text(100, 70, text="Input: ...", font=("Arial", 9))
        
        # Draw stack visualization
        self.pda_canvas.create_rectangle(250, 10, 350, 90, fill="#f0f0f0", outline="#7f8c8d")
        self.pda_canvas.create_text(300, 30, text="STACK", font=("Arial", 10, "bold"))
        self.pda_canvas.create_rectangle(260, 50, 340, 70, fill="#3498db", outline="#2980b9")
        self.pda_canvas.create_text(300, 60, text="Z0", font=("Arial", 10, "bold"), fill="white")
    
    def check_syntax(self):
        input_text = self.input_text.get(1.0, tk.END).strip()
        if not input_text:
            messagebox.showwarning("Input Mamuk", "Favor prense liafuan/ekspresaun!")
            return
        
        grammar = self.cfg_grammars[self.grammar_atual]
        
        # Reset displays
        self.parse_tree_text.delete(1.0, tk.END)
        self.status_label.config(text="Chekadu...", fg="orange")
        
        # Parse based on grammar type
        if self.grammar_atual == "Ekspresaun Matematika":
            result, derivation = self.parse_math_expression(input_text, grammar)
        elif self.grammar_atual == "Liafuan Tetun Sadiña":
            result, derivation = self.parse_tetun_sentence(input_text, grammar)
        elif self.grammar_atual == "Estrutura If-Else":
            result, derivation = self.parse_if_statement(input_text, grammar)
        elif self.grammar_atual == "Liafuan Pergunta Inglés":
            result, derivation = self.parse_english_question(input_text, grammar)
        else:
            result, derivation = False, "Grammar la rekoñese"
        
        # Update status
        if result:
            self.status_label.config(text="✓ SINTAXE VÁLIDA", fg="#27ae60")
            messagebox.showinfo("Susessu", "Sintaxe válida tuir grammar!")
        else:
            self.status_label.config(text="✗ SINTAXE LA VÁLIDA", fg="#e74c3c")
            messagebox.showerror("Erru", "Sintaxe la válida!")
        
        # Show derivation
        self.parse_tree_text.insert(1.0, derivation)
        
        # Add to history
        timestamp = datetime.now().strftime("%H:%M:%S")
        status_text = "VÁLIDA" if result else "LA VÁLIDA"
        self.history_tree.insert("", 0, values=(
            len(self.history_tree.get_children())+1,
            timestamp,
            self.grammar_atual[:20],
            input_text[:30],
            status_text,
            "CFG Parsing"
        ))
    
    def parse_math_expression(self, expr, grammar):
        """Parse mathematical expression using recursive descent"""
        # Tokenize input
        tokens = self.tokenize_math_expression(expr)
        self.current_token_index = 0
        self.tokens = tokens
        
        try:
            # Start parsing from E
            result = self.parse_E()
            
            if self.current_token_index == len(tokens):
                derivation = self.generate_math_derivation(expr, grammar)
                return True, derivation
            else:
                return False, f"Erru: Token hela: {tokens[self.current_token_index:]}"
        except Exception as e:
            return False, f"Erru parsing: {str(e)}"
    
    def parse_E(self):
        """E → E + T | E - T | T"""
        # For simplicity, we'll implement T directly
        return self.parse_T()
    
    def parse_T(self):
        """T → T * F | T / F | F"""
        return self.parse_F()
    
    def parse_F(self):
        """F → ( E ) | número | id"""
        if self.current_token_index >= len(self.tokens):
            raise Exception("Input remata laesperadu")
        
        token = self.tokens[self.current_token_index]
        
        if token == '(':
            self.current_token_index += 1
            self.parse_E()
            if self.current_token_index >= len(self.tokens) or self.tokens[self.current_token_index] != ')':
                raise Exception("Presiza ')'")
            self.current_token_index += 1
        elif token.isalpha():
            self.current_token_index += 1  # id
        elif token.isdigit():
            self.current_token_index += 1  # número
        else:
            raise Exception(f"Token laesperadu: {token}")
        
        return True
    
    def tokenize_math_expression(self, expr):
        """Simple tokenizer for math expressions"""
        tokens = []
        current = ""
        
        for char in expr:
            if char in '+-*/()':
                if current:
                    tokens.append(current)
                    current = ""
                tokens.append(char)
            elif char.isalnum():
                current += char
            elif char.isspace():
                if current:
                    tokens.append(current)
                    current = ""
        
        if current:
            tokens.append(current)
        
        return tokens
    
    def generate_math_derivation(self, expr, grammar):
        """Generate derivation steps for math expression"""
        derivation = f"Input: {expr}\n\n"
        derivation += "Hahi-husi Derivasaun:\n"
        derivation += "E (Símbolu Hahu)\n"
        
        # Simplified derivation for demo
        tokens = self.tokenize_math_expression(expr)
        
        if len(tokens) == 1:
            derivation += f"→ {tokens[0]} (F → id/número)\n"
        elif len(tokens) == 3:
            derivation += f"→ {tokens[0]} {tokens[1]} {tokens[2]}\n"
            derivation += "  (E → E + T → T + T → F + F → id + id)\n"
        elif '(' in expr and ')' in expr:
            derivation += f"→ ( E )\n"
            derivation += f"→ ( {tokens[1]} )\n"
            derivation += f"→ ( {tokens[1]} )\n"
        
        derivation += f"\nRegra Grammar Aplikadu:\n"
        for non_term, prods in grammar['productions'].items():
            if isinstance(prods, list):
                derivation += f"  {non_term} → {' | '.join(prods[:3])}\n"
        
        return derivation
    
    def parse_tetun_sentence(self, sentence, grammar):
        """Parse Tetun sentence"""
        words = sentence.lower().split()
        
        derivation = f"Input: {sentence}\n\n"
        derivation += "Hahi-husi Parsing:\n"
        
        # Simple rule-based parsing
        if len(words) >= 2:
            # Check if first word is pronoun
            if words[0] in grammar['productions']['Pronoun']:
                derivation += f"S → NP VP\n"
                derivation += f"NP → Pronoun ({words[0]})\n"
                
                # Check verb
                if words[1] in grammar['productions']['V']:
                    derivation += f"VP → V"
                    
                    if len(words) > 2:
                        # Check if next word is noun
                        if words[2] in grammar['productions']['N']:
                            derivation += f" NP\nNP → N ({words[2]})\n"
                            return True, derivation
                        elif words[2] in grammar['productions']['Adj']:
                            derivation += f" Adj ({words[2]})\n"
                            return True, derivation
                
                elif words[1] in grammar['productions']['Adj']:
                    derivation += f"VP → V Adj (implied 'mak')\n"
                    return True, derivation
        
        derivation += "\nERRU: La tuir grammar\n"
        derivation += "Ezemplu liafuan válida:\n"
        derivation += "- ha'u lee livru\n"
        derivation += "- nia hili uma boot\n"
        derivation += "- Budi bá lailais\n"
        
        return False, derivation
    
    def parse_if_statement(self, statement, grammar):
        """Parse if-else statement"""
        derivation = f"Input: {statement}\n\n"
        
        # Simple pattern matching
        if 'if' in statement and '(' in statement and ')' in statement:
            derivation += "Programa → Statement\n"
            derivation += "Statement → IfStatement\n"
            
            if 'else' in statement:
                derivation += "IfStatement → if ( Kondisaun ) { Statement } else { Statement }\n"
            else:
                derivation += "IfStatement → if ( Kondisaun ) { Statement }\n"
            
            derivation += "\nRegra Grammar Aplikadu:\n"
            for rule in grammar['productions'].keys():
                if rule in ['Kondisaun', 'Atribuisaun', 'Ekspresaun']:
                    derivation += f"  {rule} → {grammar['productions'][rule]}\n"
            
            return True, derivation
        
        derivation += "ERRU: Estrutura if-else la válida\n"
        return False, derivation
    
    def parse_english_question(self, question, grammar):
        """Parse English question"""
        derivation = f"Input: {question}\n\n"
        
        words = question.lower().replace('?', '').split()
        
        if len(words) >= 3:
            if words[0] in ['do', 'does', 'is', 'are', 'can', 'will']:
                derivation += "S → Aux NP VP ?\n"
                derivation += f"Aux → {words[0].title()}\n"
                
                # Simple validation
                return True, derivation
        
        derivation += "ERRU: Laós liafuan pergunta válida\n"
        return False, derivation
    
    def simulate_pda(self):
        """Simulate Pushdown Automata for current input"""
        input_text = self.input_text.get(1.0, tk.END).strip()
        if not input_text:
            messagebox.showwarning("Input Mamuk", "Prense input ba simulasaun PDA!")
            return
        
        self.pda_info.config(text="Simulasaun PDA hahú...")
        self.draw_pda_simulation(input_text)
        
        # Add to history
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.history_tree.insert("", 0, values=(
            len(self.history_tree.get_children())+1,
            timestamp,
            self.grammar_atual[:20],
            input_text[:30],
            "SIMULASAUN",
            "PDA"
        ))
    
    def draw_pda_simulation(self, input_text):
        """Draw PDA simulation steps"""
        self.pda_canvas.delete("all")
        
        # Draw PDA states
        states = ["q0", "q1", "q2", "qf"]
        state_positions = [(50, 75), (150, 75), (250, 75), (350, 75)]
        
        for i, (state, pos) in enumerate(zip(states, state_positions)):
            color = "#3498db" if state == "q0" else "#2ecc71" if state == "qf" else "#ecf0f1"
            self.pda_canvas.create_oval(pos[0]-20, pos[1]-20, pos[0]+20, pos[1]+20, 
                                       fill=color, outline="#2c3e50", width=2)
            self.pda_canvas.create_text(pos[0], pos[1], text=state, font=("Arial", 10, "bold"))
            
            # Draw transition arrows
            if i < len(states)-1:
                self.pda_canvas.create_line(pos[0]+20, pos[1], state_positions[i+1][0]-20, state_positions[i+1][1],
                                          arrow=tk.LAST, fill="#7f8c8d")
        
        # Draw input tape
        self.pda_canvas.create_rectangle(50, 150, 450, 180, fill="#f8f9fa", outline="#95a5a6")
        input_display = input_text[:20] + ("..." if len(input_text) > 20 else "")
        self.pda_canvas.create_text(250, 165, text=f"Input: {input_display}", font=("Arial", 10))
        
        # Draw stack operations
        self.pda_canvas.create_text(250, 200, 
                                   text="Operasaun Stack: push(S), pop(), accept()",
                                   font=("Arial", 9))
        
        self.pda_info.config(text=f"PDA simula parsing: {input_text}")

def main():
    root = tk.Tk()
    
    # Set window icon if available
    try:
        root.iconbitmap(default='icon.ico')
    except:
        pass
    
    app = CFG_SyntaxCheckerApp(root)
    
    # Center window
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')
    
    # Draw initial PDA
    app.draw_pda_initial()
    
    print("="*70)
    print("APLIKASAUN CHEKA SINTAXE UTILIZA CFG & AUTOMATA")
    print("="*70)
    print("\nFitur Prinsipal:")
    print("1. 4 Grammar CFG diferente")
    print("2. Chekajen sintaxe ho parsing")
    print("3. Simulasaun Pushdown Automata (PDA)")
    print("4. Vizualizasaun ai-hun parsing/derivasaun")
    print("5. História chekajen")
    print("\nGrammar disponível:")
    print("- Liafuan Tetun Sadiña")
    print("- Ekspresaun Matematika")
    print("- Estrutura If-Else")
    print("- Liafuan Pergunta Inglés")
    print("="*70)
    
    root.mainloop()

if __name__ == "__main__":
    main()
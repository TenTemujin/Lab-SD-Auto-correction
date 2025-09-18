import argparse
import sys
import re
from datetime import datetime
from string import Template
from pathlib import Path
from typing import Set

# --- CONSTANTS ---
# Pastas a serem ignoradas durante a busca por diretórios de alunos.
IGNORED_FOLDERS: Set[str] = {"__pycache__", ".git", ".idea", ".vscode"}


# --- HELPER FUNCTIONS ---
def safe_filename(name: str) -> str:
    """Remove caracteres inválidos para criar um nome de arquivo seguro."""
    # Remove qualquer caractere que não seja letra, número, sublinhado ou hífen.
    return re.sub(r'[^\w-]', '_', name)


def log(msg: str, success: bool = True) -> None:
    """Imprime mensagens de log com formatação colorida (sucesso/erro)."""
    # Códigos de escape ANSI para cores no terminal
    GREEN = "\033[92m"
    RED = "\033[91m"
    RESET = "\033[0m"
    
    prefix = f"{GREEN}✅{RESET}" if success else f"{RED}❌{RESET}"
    print(f"{prefix} {msg}")


def load_template(template_path: Path) -> Template:
    """Carrega o conteúdo do arquivo de template especificado."""
    try:
        content = template_path.read_text(encoding="utf-8")
        return Template(content)
    except FileNotFoundError:
        log(f"Arquivo de template não encontrado em: {template_path}", success=False)
        sys.exit(1) # Encerra o script se o template não existir.
    except IOError as e:
        log(f"Erro ao ler o arquivo de template: {e}", success=False)
        sys.exit(1)


# --- CORE LOGIC ---
def create_correction_files(args: argparse.Namespace) -> None:
    """Função principal que itera sobre as pastas e cria os arquivos de correção."""
    base_dir = args.output_dir.resolve() # .resolve() obtém o caminho absoluto
    md_template = load_template(args.template)

    print("\n" + "="*50)
    print("🚀 Iniciando a Geração de Relatórios de Correção")
    print(f"📂 Diretório Base: {base_dir}")
    print(f"📄 Atividade: {args.activity_name}")
    print(f"🧑‍🏫 Corretor: {args.grader}")
    print("="*50 + "\n")

    if not base_dir.is_dir():
        log(f"O diretório base '{base_dir}' não existe ou não é um diretório.", success=False)
        return

    student_dirs_found = 0
    for item in base_dir.iterdir():
        # Pula arquivos e pastas ignoradas
        if not item.is_dir() or item.name in IGNORED_FOLDERS:
            continue
        
        student_dirs_found += 1
        student_name = item.name
        safe_name = safe_filename(student_name)
        
        base_name = f"{safe_name}_{args.activity_name}_correction"
        correction_folder = item / base_name
        md_file_path = correction_folder / f"{base_name}.md"
        src_folder_path = correction_folder / "src"

        try:
            # Cria as pastas de correção e 'src' (exist_ok=True evita erro se já existirem)
            src_folder_path.mkdir(parents=True, exist_ok=True)
            
            # Preenche as variáveis do template
            content_to_write = md_template.substitute(
                activity_title=args.activity_title,
                grader_name=args.grader,
                student_name=student_name,
                correction_date=datetime.now().strftime("%Y-%m-%d"),
                final=args.default_grade,
            )

            # Escreve o arquivo Markdown
            md_file_path.write_text(content_to_write, encoding="utf-8")
            log(f"Estrutura de correção criada para '{student_name}' em: {correction_folder}")

        except OSError as e:
            log(f"Erro ao criar estrutura para '{student_name}': {e}", success=False)
    
    if student_dirs_found == 0:
        log("Nenhum diretório de aluno encontrado para processar.", success=False)

    print("\n" + "="*50)
    print("✨ Processo concluído!")
    print("="*50)


# --- SCRIPT ENTRY POINT ---
def main():
    """Analisa os argumentos da linha de comando e inicia o script."""
    parser = argparse.ArgumentParser(
        description="Ferramenta para criar estruturas de correção para atividades de alunos.",
        formatter_class=argparse.HelpFormatter
    )

    parser.add_argument(
        "activity_name",
        type=str,
        help="Nome ou número da atividade (ex: 'Exp01', 'Lab_AND_Gate'). Usado nos nomes dos arquivos."
    )
    parser.add_argument(
        "-t", "--activity-title",
        type=str,
        help="Título completo da atividade para o cabeçalho do relatório. Se não for fornecido, usa o 'activity_name'.",
        default=None
    )
    parser.add_argument(
        "-o", "--output-dir",
        type=Path,
        default=Path("."),
        help="Diretório base contendo as pastas dos alunos. Padrão: diretório atual."
    )
    parser.add_argument(
        "-g", "--grader",
        type=str,
        default="Nome do Corretor",
        help="Nome do corretor a ser inserido no relatório."
    )
    parser.add_argument(
        "-d", "--default-grade",
        type=str,
        default="[INSERIR NOTA]",
        help="Valor padrão para o campo da nota final."
    )
    parser.add_argument(
        "--template",
        type=Path,
        default=Path("template.md"),
        help="Caminho para o arquivo de template Markdown. Padrão: 'template.md' no mesmo diretório."
    )

    args = parser.parse_args()

    # Se o título não for fornecido, usa o nome da atividade como padrão.
    if args.activity_title is None:
        args.activity_title = args.activity_name.replace('_', ' ').title()

    create_correction_files(args)


if __name__ == "__main__":
    main()
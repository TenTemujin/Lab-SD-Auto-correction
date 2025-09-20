import argparse
import asyncio
import sys
from pathlib import Path

from markdown_it import MarkdownIt
from mdit_py_plugins.front_matter import front_matter_plugin
from mdit_py_plugins.texmath import texmath_plugin 

from pyppeteer import launch

# --- HTML TEMPLATE ---
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{title}</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.min.css" 
          integrity="sha384-GvrOXuhMATgEsSwCs4smul74iXGOixntILdUW9XmUC6+HX0sLNAK3q71HotJqlAn" 
          crossorigin="anonymous">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/github-markdown-css/5.2.0/github-markdown.min.css">
    <style>
        .markdown-body {{
            box-sizing: border-box;
            min-width: 200px;
            max-width: 980px;
            margin: 0 auto;
            padding: 45px;
        }}
        @media (max-width: 767px) {{
            .markdown-body {{
                padding: 15px;
            }}
        }}
    </style>
</head>
<body class="markdown-body">
    {content}
</body>
</html>
"""

# --- HELPER FUNCTION ---
def log(msg: str, success: bool = True, indent: int = 0) -> None:
    GREEN, RED, YELLOW, RESET = "\033[92m", "\033[91m", "\033[93m", "\033[0m"
    prefix = f"{GREEN}✅{RESET}" if success else (f"{YELLOW}ℹ️{RESET}" if success is None else f"{RED}❌{RESET}")
    print(f"{'  ' * indent}{prefix} {msg}")

# --- CORE LOGIC ---
async def convert_file_to_pdf(md_path: Path, browser):
    pdf_path = md_path.with_suffix(".pdf")
    log(f"Processando '{md_path.name}'...", success=None, indent=1)

    try:
        # Plugin de matemática sem argumento extra
        md_converter = (
            MarkdownIt("gfm-like")
            .use(front_matter_plugin)
            .use(texmath_plugin)  # ✅ sem argumento
        )
        
        markdown_text = md_path.read_text(encoding="utf-8")
        html_content = md_converter.render(markdown_text)
        final_html = HTML_TEMPLATE.format(title=md_path.stem, content=html_content)
        
        page = await browser.newPage()
        await page.setContent(final_html)
        await page.pdf({
            "path": str(pdf_path),
            "format": "A4",
            "printBackground": True,
            "margin": {"top": "2.5cm", "right": "2.5cm", "bottom": "2.5cm", "left": "2.5cm"},
        })
        await page.close()
        
        log(f"Convertido com sucesso para '{pdf_path.name}'", success=True, indent=2)
        return True

    except Exception as e:
        log(f"Falha na conversão de '{md_path.name}'", success=False, indent=2)
        log(f"Erro: {e}", success=False, indent=3)
        return False

async def main_converter(base_dir: Path):
    print("\n" + "="*50)
    print("🚀 Iniciando Conversão de Markdown para PDF")
    print(f"📂 Diretório de Busca: {base_dir.resolve()}")
    print("="*50 + "\n")

    markdown_files = list(base_dir.rglob("*.md"))
    if not markdown_files:
        log("Nenhum arquivo Markdown (.md) foi encontrado para conversão.", success=None)
        print("\n✨ Processo concluído!")
        return

    log(f"Encontrados {len(markdown_files)} arquivos Markdown para processar.")
    log("Iniciando o navegador headless (pode demorar na primeira vez)...", success=None)
    
    browser = None
    try:
        browser = await launch(headless=True, args=['--no-sandbox'])
        
        success_count = 0
        fail_count = 0

        tasks = [convert_file_to_pdf(md_path, browser) for md_path in markdown_files]
        results = await asyncio.gather(*tasks)

        for result in results:
            if result:
                success_count += 1
            else:
                fail_count += 1

    except Exception as e:
        log("Ocorreu um erro ao iniciar o navegador ou processar os arquivos.", success=False)
        log(f"Erro: {e}", success=False)
        
    finally:
        if browser:
            await browser.close()
            log("Navegador headless fechado.", success=None)

    print("\n" + "="*50)
    print("✨ Processo de conversão concluído!")
    log(f"Sucessos: {success_count}", success=True)
    log(f"Falhas: {fail_count}", success=False)
    print("="*50)


# --- SCRIPT ENTRY POINT ---
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Ferramenta para converter arquivos Markdown (.md) em PDF usando Pyppeteer.",
        formatter_class=argparse.HelpFormatter
    )
    parser.add_argument(
        "base_dir",
        type=Path,
        nargs='?',
        default=Path("."),
        help="Diretório base para buscar arquivos .md recursivamente. Padrão: diretório atual."
    )
    args = parser.parse_args()

    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        
    asyncio.run(main_converter(args.base_dir))

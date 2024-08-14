import re
from typing import List, Tuple, Dict
from rich.console import Console
from rich.live import Live
from rich.table import Table
import time

console = Console()

class TaskManager:
    def __init__(self, llm_connector):
        self.llm_connector = llm_connector

    def parse_template(self, content: str) -> Tuple[str, List[Dict[str, str]]]:
        sections = []
        template = content

        def replace_section(match):
            nonlocal sections
            section_content = match.group(1).strip()
            if (section_content.startswith('"') and section_content.endswith('"')) or \
               (section_content.startswith("'") and section_content.endswith("'")):
                section_content = section_content[1:-1]
            section_name = f"Section {len(sections) + 1}"
            sections.append({"name": section_name, "content": section_content})
            return f"${len(sections)}"

        template = re.sub(r'\{\{([^}]*)\}\}', replace_section, template)

        return template, sections

    def generate_status_table(self, section_number, elapsed_time):
        table = Table.grid(padding=(0, 1))
        table.add_row(
            f"[bold green]Processing section {section_number}...",
            f"[bold blue]Elapsed time: {elapsed_time:.3f}s"
        )
        return table

    def process_section(self, section: str, prompt: str, section_number: int, debug: bool) -> str:
        full_prompt = f"{prompt}\n\nSection task: {section}"
        response = ""
        start_time = time.time()
        
        if debug:
            with Live(self.generate_status_table(section_number, 0), refresh_per_second=10) as live:
                for chunk in self.llm_connector.send_prompt(full_prompt, debug):
                    response += chunk
                    elapsed_time = time.time() - start_time
                    live.update(self.generate_status_table(section_number, elapsed_time))
        else:
            for chunk in self.llm_connector.send_prompt(full_prompt, debug):
                response += chunk

        return response

    def execute_tasks(self, template: str, sections: List[Dict[str, str]], prompt: str, debug: bool) -> str:
        results = []
        for i, section in enumerate(sections, 1):
            result = self.process_section(section["content"], prompt, i, debug)
            results.append(result)
            if debug:
                console.print(f"[bold green]Section {i} completed.[/bold green]")

        for i, result in enumerate(results, 1):
            template = template.replace(f"${i}", result)

        return template

    def compile_results(self, template: str, sections: List[Dict[str, str]], prompt: str, debug: bool) -> str:
        return self.execute_tasks(template, sections, prompt, debug)
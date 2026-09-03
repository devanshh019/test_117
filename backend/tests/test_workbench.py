import unittest
import os
import json
from pathlib import Path

from backend.router import router
from backend.model_manager import load_models, save_model, get_model_for_task
from backend.document_generator import doc_service, py_executor, DocxSpec, PptxSpec, XlsxSpec, PySpec, CellRule, SectionSpec, SlideSpec
from backend.multimodal_vision import vision_engine
from backend.knowledge_base import knowledge_base
from backend.network_guard import sentinel
from backend.engine import agent_engine, SovereignAgentEngine
from backend.tools import tool_registry, ToolResult


class TestSovereignWorkbench(unittest.TestCase):

    def test_01_router_multi_model_auto_selection(self):
        """Verify dynamic router classifies tasks and auto-selects specialized models"""
        res_code = router.route_task("Write a python script to simulate heat exchanger LMTD and calculate heat duty")
        self.assertEqual(res_code.task_category, "ENGINEERING_MATH_AND_CODE")
        expected_code_model = get_model_for_task("ENGINEERING_MATH_AND_CODE").get("id")
        self.assertEqual(res_code.selected_model_id, expected_code_model)

        res_vision = router.route_task("Inspect P&ID for crude-free blast train, identify all control valves, transmit, check bypass")
        self.assertEqual(res_vision.task_category, "MULTIMODAL_IMAGE_INSPECTION")
        expected_vision_model = get_model_for_task("MULTIMODAL_IMAGE_INSPECTION").get("id")
        self.assertEqual(res_vision.selected_model_id, expected_vision_model)

        res_doc = router.route_task("Generate a Word document approval note and PowerPoint presentation deck")
        self.assertEqual(res_doc.task_category, "ENTERPRISE_DELIVERABLE_SYNTHESIS")
        expected_doc_model = get_model_for_task("ENTERPRISE_DELIVERABLE_SYNTHESIS").get("id")
        self.assertEqual(res_doc.selected_model_id, expected_doc_model)

    def test_02_sandbox_code_execution(self):
        """Verify isolated Python sandbox execution and Matplotlib artifact generation"""
        script = (
            "import matplotlib.pyplot as plt\n"
            "x = [1, 2, 3, 4]\n"
            "y = [10, 20, 15, 30]\n"
            "plt.plot(x, y)\n"
            "print('SANDBOX_CALC_OK:42')\n"
        )
        spec = PySpec(title="test_sim", code=script, timeout_seconds=15)
        out_file = Path("backend/data/storage/test_sim.py")
        deliv = py_executor.deliver(spec, out_file)
        self.assertTrue(deliv.execution.success)
        self.assertIn("SANDBOX_CALC_OK:42", deliv.execution.stdout)
        self.assertTrue(len(deliv.execution.plots) > 0)
        if out_file.exists():
            os.remove(out_file)

    def test_03_industry_standard_document_service_and_renderers(self):
        """Verify Schema validation -> Strategy Renderer -> DocumentResult architecture"""
        # 1. DOCX Renderer with DocxSpec
        docx_spec = DocxSpec(
            title="Technical Note",
            subject="Evaluation",
            sections=[SectionSpec(heading="Executive Summary", content="Sample paragraph content.")]
        )
        docx_res = doc_service.generate(docx_spec)
        self.assertTrue(os.path.exists(docx_res.path))
        self.assertTrue(docx_res.size_bytes > 5000)

        # 2. XLSX Renderer with XlsxSpec and Data-Driven CellRules
        xlsx_spec = XlsxSpec(
            title="Calculations",
            headers=["Parameter", "Design Value", "Calculated Value", "Unit", "Status"],
            rows=[
                ["Internal Pressure", 2.5, 2.5, "MPa", "VERIFIED"],
                ["Allowable Stress", 138.0, 138.0, "MPa", "VERIFIED"],
                ["Corrosion Rate", 0.15, 0.45, "mm/yr", "FLAGGED"]
            ],
            rules=[
                CellRule(match_values=["VERIFIED"], color_hex="16A34A", bold=True),
                CellRule(match_values=["FLAGGED"], color_hex="DC2626", bold=True),
            ]
        )
        xlsx_res = doc_service.generate(xlsx_spec)
        self.assertTrue(os.path.exists(xlsx_res.path))
        self.assertTrue(xlsx_res.size_bytes > 4000)

        # 3. PPTX Renderer with PptxSpec
        pptx_spec = PptxSpec(
            title="Board Deck",
            subtitle="Subtitle",
            slides=[SlideSpec(title="Overview", bullets=["Point 1", "Point 2"])]
        )
        pptx_res = doc_service.generate(pptx_spec)
        self.assertTrue(os.path.exists(pptx_res.path))
        self.assertTrue(pptx_res.size_bytes > 10000)

    def test_04_dynamic_rag_pipeline(self):
        """Verify dynamic file ingestion, chunking, and similarity search in RAG"""
        import tempfile
        test_text = "API 510 Section 7.1 specifies calculation of corrosion rate and remaining life: Cr = (t_initial - t_actual) / Time. If remaining life is under 2 years, immediate maintenance turnaround is required."
        with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False) as tf:
            tf.write(test_text)
            temp_path = tf.name

        try:
            doc_res = knowledge_base.ingest_file(
                file_path=temp_path,
                original_filename="Temporary_Test_Standard.txt"
            )
            self.assertTrue(doc_res["success"])
            self.assertTrue(doc_res["indexed_chunks"] >= 1)

            search_results = knowledge_base.search("API 510 corrosion rate turnaround", top_k=2)
            self.assertTrue(len(search_results) > 0)
            self.assertIn("remaining life", search_results[0]["excerpt"].lower())

            # Clean up test document so persistent DB is not polluted
            knowledge_base.delete_document(doc_res["doc_id"])
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)

    def test_05_air_gap_sentinel_proof(self):
        """Verify zero external egress and cryptographic audit chain"""
        status = sentinel.get_security_status()
        self.assertEqual(status["outbound_egress_bytes"], 0)
        self.assertEqual(status["external_dns_queries"], 0)
        self.assertTrue(status["air_gap_enforced"])
        self.assertTrue(len(status["latest_audit_hash"]) == 64)

        cert = sentinel.generate_sovereign_certificate()
        self.assertTrue(cert["air_gap_verified"])
        self.assertIn("ZERO EGRESS", cert["external_egress_verified"])

    def test_06_agent_execution_with_rag(self):
        """Verify complete agent execution pipeline using dynamic RAG knowledge"""
        prompt = "Draft a formal Word document report regarding API 510 remaining life standards and calculate corrosion rates."
        res = agent_engine.execute_task(prompt)
        self.assertIn("task_id", res)
        self.assertTrue(len(res["steps"]) >= 2)
        self.assertEqual(res["sovereign_proof"]["outbound_bytes"], 0)

    def test_07_react_tool_registry_and_execution(self):
        """Verify tool registry definitions and execution for all registered tools"""
        defs = tool_registry.get_definitions()
        tool_names = [d.name for d in defs]
        self.assertIn("search_knowledge_base", tool_names)
        self.assertIn("execute_python_code", tool_names)
        self.assertIn("generate_word_document", tool_names)
        self.assertIn("generate_powerpoint_presentation", tool_names)
        self.assertIn("generate_excel_spreadsheet", tool_names)
        self.assertIn("inspect_visual_attachment", tool_names)

        calc_res = tool_registry.execute_tool(
            "execute_python_code",
            {"code": "import math\nr = math.sqrt(144)\nprint(f'RADIUS_RESULT:{r}')"}
        )
        self.assertTrue(calc_res.success)
        self.assertIn("RADIUS_RESULT:12.0", calc_res.output)

        excel_res = tool_registry.execute_tool(
            "generate_excel_spreadsheet",
            {
                "title": "Dynamic Hydrotest Matrix",
                "sheet_name": "Hydrotest",
                "headers": ["Test ID", "Test Medium", "Design Pressure (bar)", "Hydrotest Pressure (bar)", "Status"],
                "rows": [
                    ["HYD-01", "Demineralized Water", 18.5, 27.75, "VERIFIED"],
                    ["HYD-02", "Nitrogen Gas", 12.0, 15.6, "ACCEPTABLE"],
                    ["HYD-03", "Standard Water", 25.0, 30.0, "FLAGGED"]
                ]
            }
        )
        self.assertTrue(excel_res.success)
        self.assertTrue(len(excel_res.deliverables) == 1)
        self.assertEqual(excel_res.deliverables[0]["file_type"], "xlsx")
        self.assertEqual(len(excel_res.deliverables[0]["rows"]), 3)

    def test_08_react_parser(self):
        """Verify ReAct parser extracts Thoughts, Actions, JSON Arguments, and Final Answers"""
        engine = SovereignAgentEngine()

        react_sample = """Thought: I should calculate the heat duty using Python.
Action: execute_python_code
Action Input: {"code": "q = 500 * 4.184 * 35\\nprint(f'HEAT_DUTY:{q}')"}"""

        thought, action, action_input, final = engine._parse_react_response(react_sample)
        self.assertEqual(action, "execute_python_code")
        self.assertIsNotNone(action_input)
        self.assertIn("code", action_input)
        self.assertIn("HEAT_DUTY", action_input["code"])
        self.assertIsNone(final)

        final_sample = """Thought: I have verified all ASME formulas and generated the calculation sheet.
Final Answer: The pressure vessel satisfies ASME Section VIII Div 1 requirements with minimum thickness 27.5mm."""

        thought2, action2, input2, final2 = engine._parse_react_response(final_sample)
        self.assertIsNone(action2)
        self.assertIsNotNone(final2)
        self.assertIn("ASME Section VIII Div 1", final2)

    def test_09_direct_json_and_pure_python_filter(self):
        """Verify direct JSON is never treated as Python code and routes to document tools"""
        engine = SovereignAgentEngine()

        # Direct JSON for Excel
        excel_json = """```json
{
  "title": "Corrosion Assessment",
  "headers": ["Tag", "Thickness", "Corrosion Rate", "Status"],
  "rows": [["TK-101", 12.4, 0.35, "VERIFIED"], ["TK-102", 9.1, 0.82, "FLAGGED"]]
}
```"""
        thought, action, action_input, final = engine._parse_react_response(excel_json)
        self.assertEqual(action, "generate_excel_spreadsheet")
        self.assertIsNotNone(action_input)
        self.assertEqual(len(action_input["rows"]), 2)

        # JSON should NEVER be extracted as Python code
        py_extracted = engine._extract_pure_python_code(excel_json)
        self.assertIsNone(py_extracted)

        # Pure Python block SHOULD be extracted
        real_py = """```python
import numpy as np
t = np.linspace(0, 10, 100)
print(f'TIME_LEN:{len(t)}')
```"""
        thought_py, action_py, input_py, _ = engine._parse_react_response(real_py)
        self.assertEqual(action_py, "execute_python_code")
        self.assertIn("import numpy", input_py["code"])

    def test_10_markdown_table_and_sections_parser(self):
        """Verify markdown tables and sections are cleanly parsed into structured rows and headings"""
        engine = SovereignAgentEngine()

        md_table = """Here is the inspection summary:
| Equipment | Wall Thickness (mm) | Allowable (mm) | Status |
|---|---|---|---|
| Vessel V-101 | 14.5 | 12.0 | VERIFIED |
| Boiler B-202 | 8.2 | 9.5 | FLAGGED |
"""
        table_result = engine._parse_markdown_table(md_table)
        self.assertIsNotNone(table_result)
        headers, rows = table_result
        self.assertEqual(len(headers), 4)
        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0][0], "Vessel V-101")
        self.assertEqual(rows[0][1], 14.5)

        md_doc = """## Executive Summary
Turnaround inspection completed for all primary distillation vessels.

## Engineering Findings
Wall thickness measurements on V-101 show acceptable corrosion margins.

## Recommendations
Schedule next UT inspection in 24 months.
"""
        sections = engine._parse_markdown_sections(md_doc)
        self.assertEqual(len(sections), 3)
        self.assertEqual(sections[0]["heading"], "Executive Summary")
        self.assertIn("Turnaround inspection", sections[0]["content"])
        self.assertEqual(sections[1]["heading"], "Engineering Findings")


if __name__ == "__main__":
    unittest.main()

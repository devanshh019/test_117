import unittest
import os
from pathlib import Path

from backend.router import router
from backend.model_manager import load_models, save_model, get_model_for_task
from backend.sandbox_executor import sandbox
from backend.document_generator import doc_generator
from backend.multimodal_vision import vision_engine
from backend.knowledge_base import knowledge_base
from backend.network_guard import sentinel
from backend.engine import agent_engine



class TestSovereignWorkbench(unittest.TestCase):

    def test_01_router_multi_model_auto_selection(self):
        """Verify dynamic router classifies tasks and auto-selects specialized models"""
        res_code = router.route_task("Write a python script to simulate heat exchanger LMTD and calculate heat duty")
        self.assertEqual(res_code.task_category, "ENGINEERING_MATH_AND_CODE")
        expected_math_model = get_model_for_task("ENGINEERING_MATH_AND_CODE").get("id")
        self.assertEqual(res_code.selected_model_id, expected_math_model)

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
        res = sandbox.execute(script, script_name_prefix="test_sim")
        self.assertTrue(res["success"])
        self.assertIn("SANDBOX_CALC_OK:42", res["stdout"])
        self.assertTrue(len(res["plots"]) > 0)

    def test_03_office_deliverables_generation(self):
        """Verify generation of genuine .docx, .xlsx, and .pptx files"""
        docx_res = doc_generator.generate_custom_word_doc("Technical Note", "Evaluation", ["Sample paragraph"])
        self.assertTrue(os.path.exists(doc_generator.storage_dir / docx_res["filename"]))
        self.assertTrue(docx_res["size_bytes"] > 5000)

        xlsx_res = doc_generator.generate_custom_excel("Calculations", ["Col A", "Col B"], [["Val 1", "Val 2"]])
        self.assertTrue(os.path.exists(doc_generator.storage_dir / xlsx_res["filename"]))
        self.assertTrue(xlsx_res["size_bytes"] > 4000)

        pptx_res = doc_generator.generate_custom_powerpoint("Board Deck", "Subtitle", [{"title": "Overview", "bullets": ["Point 1"]}])
        self.assertTrue(os.path.exists(doc_generator.storage_dir / pptx_res["filename"]))
        self.assertTrue(pptx_res["size_bytes"] > 10000)

    def test_04_dynamic_rag_pipeline(self):
        """Verify dynamic text ingestion, chunking, and BM25/TF-IDF similarity search in RAG"""
        doc_res = knowledge_base.ingest_text(
            title="API 510 Pressure Vessel Inspection Standard",
            text="API 510 Section 7.1 specifies calculation of corrosion rate and remaining life: Cr = (t_initial - t_actual) / Time. If remaining life is under 2 years, immediate maintenance turnaround is required.",
            category="STANDARDS"
        )
        self.assertTrue(doc_res["success"])
        self.assertTrue(doc_res["indexed_chunks"] >= 1)

        search_results = knowledge_base.search("API 510 corrosion rate turnaround", top_k=2)
        self.assertTrue(len(search_results) > 0)
        self.assertIn("API 510", search_results[0]["title"])
        self.assertIn("remaining life", search_results[0]["excerpt"].lower())

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
        self.assertTrue(len(res["steps"]) >= 3)
        self.assertEqual(res["sovereign_proof"]["outbound_bytes"], 0)

if __name__ == "__main__":
    unittest.main()


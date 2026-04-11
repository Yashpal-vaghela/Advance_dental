from django.test import TestCase
from django.urls import reverse


class SurgicalGuidePdfTests(TestCase):
    def test_post_generates_pdf_response(self):
        response = self.client.post(
            reverse("surgical_guide"),
            {
                "preferred_implant_company": "Nobel Biocare",
                "implant_name": "All-on-4",
                "jaw_information": ["maxilla", "mandible"],
                "prosthetic_plan": "Full arch rehabilitation",
                "desired_implant_location": "Upper arch",
                "preferred_size": "4.3 x 13 mm",
                "ap_spread_angle_implant": "15 degrees",
                "immediate_extractions": "True",
                "immediate_extractions_notes": "18 and 19",
                "bone_grafting": "False",
                "bone_reduction": "True",
                "bone_reduction_notes": "Minor reduction",
                "surgical_drill_kit": "Standard kit",
                "provisional_planning": "Immediate load provisional",
                "surgery_date": "2026-04-15",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/pdf")
        self.assertTrue(response.content.startswith(b"%PDF"))

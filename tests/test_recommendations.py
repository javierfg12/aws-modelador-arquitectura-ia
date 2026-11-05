import unittest

from recommendations import (
    recomendar_aplicacion,
    recomendar_datos,
    recomendar_inferencia,
    recomendar_integracion,
    recomendar_observabilidad,
    recomendar_seguridad,
    recomendar_tradeoff,
)


class RecommendationRulesTests(unittest.TestCase):
    def test_sector_changes_document_partitioning(self):
        insurance = recomendar_datos(18000, True, "Asegurador")
        retail = recomendar_datos(18000, True, "Retail")
        self.assertIn("tipo de siniestro", insurance)
        self.assertIn("tipo documental", retail)

    def test_low_volume_uses_basic_storage(self):
        self.assertIn("S3 estándar", recomendar_datos(100, False, "Educación"))

    def test_sensitive_data_adds_security_controls(self):
        result = recomendar_seguridad(True, "Medio")
        self.assertIn("KMS", result)
        self.assertIn("CloudTrail", result)

    def test_low_budget_prioritizes_native_controls(self):
        result = recomendar_seguridad(True, "Bajo")
        self.assertIn("controles nativos", result)

    def test_inference_choice_follows_strategy(self):
        self.assertIn("Bedrock", recomendar_inferencia("Gestionado"))
        self.assertIn("SageMaker", recomendar_inferencia("Control fino"))

    def test_latency_and_concurrency_change_integration(self):
        result = recomendar_integracion(3, 220)
        self.assertIn("caché", result)
        self.assertIn("220 usuarios", result)
        basic = recomendar_integracion(8, 20)
        self.assertNotIn("caché", basic)
        self.assertNotIn("auto-scaling", basic)

    def test_demand_volatility_changes_observability(self):
        high = recomendar_observabilidad("Alta", "Medio")
        low = recomendar_observabilidad("Baja", "Medio")
        self.assertIn("Cost Anomaly Detection", high)
        self.assertNotIn("Cost Anomaly Detection", low)

    def test_savings_plans_are_conditional(self):
        result = recomendar_observabilidad("Alta", "Bajo")
        self.assertIn("cómputo elegible", result)
        self.assertIn("demanda estable", result)

    def test_recovery_targets_are_included(self):
        result = recomendar_aplicacion("Alta", 4, 1)
        self.assertIn("RTO ≤4 h", result)
        self.assertIn("RPO ≤1 h", result)

    def test_tradeoff_reflects_model_control(self):
        managed = recomendar_tradeoff("Gestionado", True, "Medio")
        controlled = recomendar_tradeoff("Control fino", False, "Alto")
        self.assertIn("Bedrock", managed)
        self.assertIn("SageMaker", controlled)


if __name__ == "__main__":
    unittest.main()

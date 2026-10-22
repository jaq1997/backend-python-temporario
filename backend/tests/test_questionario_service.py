import unittest
from unittest.mock import patch

from app.services import questionario_service


class QuestionarioServiceTests(unittest.TestCase):
    def setUp(self):
        self.perguntas = [{"id": "1"}, {"id": "2"}, {"id": "3"}]
        self.indice = {
            "1": {"a": "cardiaca"},
            "2": {"b": "respiratoria"},
            "3": {"c": "sono"},
        }
        self.respostas = {"1": "a", "2": "b", "3": "c"}
        self.patches = [
            patch.object(questionario_service, "PERGUNTAS", self.perguntas),
            patch.object(questionario_service, "_INDICE", self.indice),
        ]
        for item in self.patches:
            item.start()
            self.addCleanup(item.stop)

    def test_returns_tie_for_frontend_to_present_as_choices(self):
        resultado = questionario_service.calcular_resultado(self.respostas)

        self.assertTrue(resultado["empate"])
        self.assertIsNone(resultado["jornada_recomendada"])
        self.assertEqual(
            resultado["jornadas_empatadas"],
            ["cardiaca", "respiratoria", "sono"],
        )
        self.assertEqual(
            resultado["pontuacao"],
            {"cardiaca": 1, "respiratoria": 1, "sono": 1},
        )

    def test_validates_selected_journey_when_resolving_tie(self):
        resultado = questionario_service.calcular_resultado(
            self.respostas,
            jornada_escolhida="respiratoria",
        )

        self.assertEqual(resultado["jornada_recomendada"], "respiratoria")
        self.assertTrue(resultado["empate"])

    def test_rejects_journey_not_in_tie(self):
        with self.assertRaises(ValueError):
            questionario_service.calcular_resultado(
                self.respostas,
                jornada_escolhida="invalida",
            )


if __name__ == "__main__":
    unittest.main()

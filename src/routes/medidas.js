var express = require("express");
var router = express.Router();

var medidaController = require("../controllers/medidaController");

router.get("/ultimas/:idAquario", function (req, res) {
    medidaController.buscarUltimasMedidas(req, res);
});

router.get("/tempo-real/:idAquario", function (req, res) {
    medidaController.buscarMedidasEmTempoReal(req, res);
})

router.get("/PorcentagemRAM/:fkTorre", function (req, res) {
    medidaController.buscarPorcentagemRAM(req, res);
})

router.get("/PorcentagemPercaPacotes/:fkTorre", function (req, res) {
    medidaController.buscarPorcentagemPercaPacotes(req, res);
})

router.get("/DataHora/:fkTorre", function (req, res) {
    medidaController.buscarDataHora(req, res);
})


module.exports = router;
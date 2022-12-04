var express = require("express");
var router = express.Router();

var medidaController = require("../controllers/medidaController");

router.get("/ultimas/:idAquario", function (req, res) {
    medidaController.buscarUltimasMedidas(req, res);
});

router.get("/tempo-real/:fkTorre/:fkComponente", function (req, res) {
    medidaController.buscarMedidasEmTempoReal(req, res);
})

router.get("/PorcentagemCPU/:fkTorre", function (req, res) {
    medidaController.buscarPorcentagemCPU(req, res);
})

router.get("/PorcentagemRAM/:fkTorre", function (req, res) {
    medidaController.buscarPorcentagemRAM(req, res);
})

router.get("/PorcentagemDisco/:fkTorre", function (req, res) {
    medidaController.buscarPorcentagemDisco(req, res);
})

router.get("/PorcentagemPercaPacotes/:fkTorre", function (req, res) {
    medidaController.buscarPorcentagemPercaPacotes(req, res);
})


router.get("/DataHora/:fkTorre", function (req, res) {
    medidaController.buscarDataHora(req, res);
})

router.get("/Registro/:fkTorre/:nmrComponentes", function (req, res) {
    medidaController.buscarRegistro(req, res);
})

router.get("/BuscarProc/:fkTorre", function (req, res) {
    medidaController.buscarProc(req, res);
})

router.get("/Metrica/buscarMetrica/:fkEmpresa/:nmrComponentes", function (req, res) {
    medidaController.buscarMetrica(req, res);
})

router.get("/Temperatura/:fkTorre", function (req, res) {
    medidaController.buscarTemperatura(req, res);
})

router.get("/PlacaMae/:fkTorre", function (req, res) {
    medidaController.buscarPlacaMae(req, res);
})

router.get("/Desempenho/:fkTorre", function (req, res) {
    medidaController.buscarPlacaMae(req, res);
})

module.exports = router;
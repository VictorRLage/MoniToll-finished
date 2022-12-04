
router.get("/Temperatura/:fkTorre", function (req, res) {
    medidaController.buscarTemperatura(req, res);
})

router.get("/PlacaMae/:fkTorre", function (req, res) {
    medidaController.buscarPlacaMae(req, res);
})

router.get("/Desempenho/:fkTorre", function (req, res) {
    medidaController.buscarPlacaMae(req, res);
})

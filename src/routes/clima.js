var express = require("express");
var router = express.Router();

var climaController = require("../controllers/climaController");

// router.get("/", function (req, res) {
//     climaController.testar(req, res);
// });

// router.get("/listar", function (req, res) {
//     climaController.listar(req, res);
// });

// router.get("/listar/:idUsu", function (req, res) {
//     climaController.listarPorUsuario(req, res);
// });

router.post("/inserir", function (req, res) {
    climaController.inserir(req, res);
});
router.get("/listar/:fkLugar", function (req, res) {
    climaController.tempLocal(req, res);
});
router.get("/semana/:fkLugar", function(req, res){
    climaController.tempSemana(req, res);
})

module.exports = router;
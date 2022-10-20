var express = require("express");
var router = express.Router();

var usuarioController = require("../controllers/usuarioController");

router.get("/", function (req, res) {
    usuarioController.testar(req, res);
});

router.get("/listar", function (req, res) {
    usuarioController.listar(req, res);
});

//Recebendo os dados do html e direcionando para a função cadastrar de usuarioController.js
router.post("/cadastrar", function (req, res) {
    usuarioController.cadastrar(req, res);
})

router.post("/cadastrarEmp", function (req, res) {
    usuarioController.cadastrarEmp(req, res);
})

router.post("/atualizarAdm", function (req, res) {
    usuarioController.atualizarAdm(req, res);
})

router.post("/autenticar", function (req, res) {
    usuarioController.entrar(req, res);
});

router.post("/verificarTorres", function (req, res) {
    usuarioController.verificarTorres(req, res);
});

module.exports = router;
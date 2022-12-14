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

router.post("/verificarPlano", function (req, res) {
    usuarioController.verificarPlano(req, res);
});

router.post("/CadastrarTorre", function (req, res) {
    usuarioController.CadastrarTorre(req, res);
});

router.post("/CadastrarComponente", function (req, res) {
    usuarioController.CadastrarComponente(req, res);
});

router.post("/UltimaTorre", function (req, res) {
    usuarioController.UltimaTorre(req, res);
});

router.post("/ObterComponentes", function (req, res) {
    usuarioController.ObterComponentes(req, res);
});

router.post("/cadastrarUsuario", function (req, res) {
    usuarioController.CadastrarUsuario(req, res);
});

router.post("/ObterDadosTorre", function (req, res) {
    usuarioController.ObterDadosTorre(req, res);
});

router.post("/ObterNomeEmp", function (req, res) {
    usuarioController.ObterNomeEmp(req, res);
});

router.post("/CadastrarProcessoMatar", function (req, res) {
    usuarioController.CadastrarProcessoMatar(req, res);
});

router.post("/CadastrarProcessoMorto", function (req, res) {
    usuarioController.CadastrarProcessoMorto(req, res);
});

router.post("/CadastrarProcessoConfiavel", function (req, res) {
    usuarioController.CadastrarProcessoConfiavel(req, res);
});

router.post("/VerificarProcesso", function (req, res) {
    usuarioController.VerificarProcesso(req, res);
});

router.post("/cadastrarMetrica", function (req, res) {
    usuarioController.cadastrarMetrica(req, res);
});

router.post("/ObterAlertasTorre", function (req, res) {
    usuarioController.ObterAlertasTorre(req, res);
});

router.post("/ObterAlertasEmpresa", function (req, res) {
    usuarioController.ObterAlertasEmpresa(req, res);
});

router.post("/ObterCriticidadeTorre", function (req, res) {
    usuarioController.ObterCriticidadeTorre(req, res);
});

router.post("/buscarPalavras", function (req, res) {
    usuarioController.buscarPalavras(req, res);
});


module.exports = router;
var express = require("express");
var router = express.Router();

var climaController = require("../controllers/climaController");

router.get("/tempLocal/:fkTorre", function (req, res) {
    climaController.tempLocal(req, res);
});
router.get("/tempSemana/:fkTorre", function(req, res){
    climaController.tempSemana(req, res);
})

module.exports = router;
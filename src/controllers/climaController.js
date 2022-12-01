var climaModel = require("../models/climaModel");

// function testar(req, res) {
//     console.log("ENTRAMOS NO climaController");
//     res.json("ENTRAMOS NO clima CONTROLLER");
// }

function tempLocal(req, res) {
    console.log("AAAAAAAAAAAAAAAAAAAAAAAAAa")
    console.log(req.params)
    var fkTorre = req.params.fkTorre;

    console.log("FK", fkTorre);
    climaModel.tempLocal(fkTorre).then(function (resultado) {
        if (resultado.length > 0) {
            res.status(200).json(resultado);
        } else {
            res.status(204).send("Nenhum resultado encontrado!")
        }
    }).catch(function (erro) {
        console.log(erro);
        console.log("Houve um erro ao buscar as ultimas medidas.", erro.sqlMessage);
        res.status(500).json(erro.sqlMessage);
    });
}

function tempSemana(req, res){
    console.log("AAAAAAAAAAAAAAAAAAAAAAAAAa")
    console.log(req.params)
    var fkTorre = req.params.fkTorre;

    console.log("FK", fkTorre);
    climaModel.tempSemana(fkTorre).then(function (resultado) {
        if (resultado.length > 0) {
            res.status(200).json(resultado);
        } else {
            res.status(204).send("Nenhum resultado encontrado!")
        }
    }).catch(function (erro) {
        console.log(erro);
        console.log("Houve um erro ao buscar as ultimas medidas.", erro.sqlMessage);
        res.status(500).json(erro.sqlMessage);
    });
}



module.exports = {
    tempLocal,
    tempSemana,
}
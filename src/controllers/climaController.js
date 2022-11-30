var climaModel = require("../models/climaModel");

// function testar(req, res) {
//     console.log("ENTRAMOS NO climaController");
//     res.json("ENTRAMOS NO clima CONTROLLER");
// }

function listar(req, res) {
    console.log("AAAAAAAAAAAAAAAAAAAAAAAAAa")
    console.log(req.params)
    var fkLocal = req.params.fkLugar;


    climaModel.buscarUltimasMedidas(fkLocal).then(function (resultado) {
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
function tempLocal(req, res) {
    console.log("AAAAAAAAAAAAAAAAAAAAAAAAAa")
    console.log(req.params)
    var fkLocal = req.params.fkLugar;

    console.log("FK", fkLocal);
    climaModel.tempLocal(fkLocal).then(function (resultado) {
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
    var fkLocal = req.params.fkLugar;

    console.log("FK", fkLocal);
    climaModel.tempSemana(fkLocal).then(function (resultado) {
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
// function listarPorUsuario(req, res) {
//     var idUsuario = req.body.idServer;

//     climaModel.listarPorUsuario(idUsuario)
//         .then(
//             function (resultado) {
//                 if (resultado.length > 0) {
//                     res.status(200).json(resultado);
//                 } else {
//                     res.status(204).send("Nenhum resultado encontrado!");
//                 }
//             }
//         )
//         .catch(
//             function (erro) {
//                 console.log(erro);
//                 console.log(
//                     "Houve um erro ao buscar os votos: ",
//                     erro.sqlMessage
//                 );
//                 res.status(500).json(erro.sqlMessage);
//             }
//         );
// }


function inserir(req, res) {
    var nomeLocal = req.body.localServer;
    // Faça as validações dos valores
    if (nomeLocal == undefined ) {
        res.status(400).send("escolha um lugar!");
    } else {
        
        // Passe os valores como parâmetro e vá para o arquivo usuarioModel.js
        climaModel.inserir(nomeLocal)
            .then(
                function (resultado) {
                    res.json(resultado);
                }
            ).catch(
                function (erro) {
                    console.log(erro);
                    console.log(
                        "\nHouve um erro ao realizar o voto! Erro: ",
                        erro.sqlMessage
                    );
                    res.status(500).json(erro.sqlMessage);
                }
            );
    }
}


module.exports = {
    // testar,
    listar,
    tempLocal,
    tempSemana,
    // listarPorUsuario,
    inserir
}
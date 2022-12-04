
function buscarTemperatura(req, res) {

    var fkTorre = req.params.fkTorre;

    console.log(`Recuperando medidas em tempo real`);

    medidaModel.buscarTemperatura(fkTorre).then(function (resultado) {
        if (resultado.length > 0) {
            res.status(200).json(resultado);
        } else {
            res.status(204).send("Nenhum resultado encontrado!")
        }
    }).catch(function (erro) {
        console.log(erro);
        console.log("Houve um erro ao buscar porcentagem perca pacotes.", erro.sqlMessage);
        res.status(500).json(erro.sqlMessage);
    });
}

function buscarPlacaMae(req, res) {

    var fkTorre = req.params.fkTorre;

    console.log(`Recuperando medidas em tempo real`);

    medidaModel.buscarPlacaMae(fkTorre).then(function (resultado) {
        if (resultado.length > 0) {
            res.status(200).json(resultado);
        } else {
            res.status(204).send("Nenhum resultado encontrado!")
        }
    }).catch(function (erro) {
        console.log(erro);
        console.log("Houve um erro ao buscar porcentagem perca pacotes.", erro.sqlMessage);
        res.status(500).json(erro.sqlMessage);
    });
}

function buscarDesempenho(req, res) {

    var fkTorre = req.params.fkTorre;

    console.log(`Recuperando medidas em tempo real`);

    medidaModel.buscarDesempenho(fkTorre).then(function (resultado) {
        if (resultado.length > 0) {
            res.status(200).json(resultado);
        } else {
            res.status(204).send("Nenhum resultado encontrado!")
        }
    }).catch(function (erro) {
        console.log(erro);
        console.log("Houve um erro ao buscar porcentagem perca pacotes.", erro.sqlMessage);
        res.status(500).json(erro.sqlMessage);
    });
}

module.exports = {
    buscarTemperatura,
    buscarPlacaMae,
    buscarDesempenho
}
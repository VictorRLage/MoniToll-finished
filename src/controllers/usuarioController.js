var usuarioModel = require("../models/usuarioModel");

var sessoes = [];

function testar(req, res) {
    console.log("ENTRAMOS NA usuarioController");
    res.json("ESTAMOS FUNCIONANDO!");
}

function listar(req, res) {
    usuarioModel.listar()
        .then(function (resultado) {
            if (resultado.length > 0) {
                res.status(200).json(resultado);
            } else {
                res.status(204).send("Nenhum resultado encontrado!")
            }
        }).catch(
            function (erro) {
                console.log(erro);
                console.log("Houve um erro ao realizar a consulta! Erro: ", erro.sqlMessage);
                res.status(500).json(erro.sqlMessage);
            }
            );
        }
        
        function entrar(req, res) {
            var email = req.body.emailServer;
            var senha = req.body.senhaServer;
            var fkPerfil = req.body.fkPerfilServer
            
            if(email == undefined) {
                res.status(400).send("Seu email está undefined!");
            } else if (senha == undefined) {
                res.status(400).send("Sua senha está indefinida!");
            }else if (fkPerfil == undefined) {
                res.status(400).send("Seu perfil está indefinido!");
            } else {
                
        usuarioModel.entrar(email, senha, fkPerfil)
            .then(
                function (resultado) {
                    console.log(`\nResultados encontrados: ${resultado.length}`);
                    console.log(`Resultados: ${JSON.stringify(resultado)}`); // transforma JSON em String

                    if (resultado.length == 1) {
                        console.log(resultado);
                        res.json(resultado[0]);
                    } else if (resultado.length == 0) {
                        res.status(403).send("Email e/ou senha inválido(s)");
                    } else {
                        res.status(403).send("Mais de um usuário com o mesmo login e senha!");
                    }
                }
            ).catch(
                function (erro) {
                    console.log(erro);
                    console.log("\nHouve um erro ao realizar o login! Erro: ", erro.sqlMessage);
                    res.status(500).json(erro.sqlMessage);
                }
            );
    }

}

function cadastrar(req, res) {
    // Crie uma variável que vá recuperar os valores do arquivo cadastro.html
    var nome = req.body.nomeServer;
    var cnpj = req.body.cnpjServer;
    var email = req.body.emailServer;
    var senha = req.body.senhaServer;
    var perfil = req.body.fkPerfilServer;

    // Faça as validações dos valores
    if (nome == undefined) {
        res.status(400).send("Seu nome está undefined!");
    } else if (cnpj == undefined) {
        res.status(400).send("Seu email está undefined!");
    } else if (email == undefined) {
        res.status(400).send("Sua senha está undefined!");
    } else if (senha == undefined) {
        res.status(400).send("Seu senha está undefined!");
    } else if (perfil == undefined) {
        res.status(400).send("Seu perfil está undefined!");
    } else {
        
        // Passe os valores como parâmetro e vá para o arquivo usuarioModel.js
        usuarioModel.cadastrar(nome, cnpj, email, senha, perfil)
            .then(
                function (resultado) {
                    res.json(resultado);
                }
            ).catch(
                function (erro) {
                    console.log(erro);
                    console.log(
                        "\nHouve um erro ao realizar o cadastro! Erro: ",
                        erro.sqlMessage
                    );
                    res.status(500).json(erro.sqlMessage);
                }
            );
    }
}

function cadastrarP(req, res) {
    // Crie uma variável que vá recuperar os valores do arquivo cadastro.html
    var idP = req.body.idPServer;
    var nomeP = req.body.nomePServer;
    var localP = req.body.localPServer;

    // Faça as validações dos valores
    if (idP == undefined) {
        res.status(400).send("Seu idP está undefined!");
    } else if (nomeP == undefined) {
        res.status(400).send("Seu nomeP está undefined!");
    } else if (localP == undefined) {
        res.status(400).send("Seu localP está undefined!");
    } else {
        
        // Passe os valores como parâmetro e vá para o arquivo usuarioModel.js
        usuarioModel.cadastrarP(idP, nomeP, localP)
            .then(
                function (resultado) {
                    res.json(resultado);
                }
            ).catch(
                function (erro) {
                    console.log(erro);
                    console.log(
                        "\nHouve um erro ao realizar o cadastro! Erro: ",
                        erro.sqlMessage
                    );
                    res.status(500).json(erro.sqlMessage);
                }
            );
    }
}

function atualizar(req, res) {
    // Crie uma variável que vá recuperar os valores do arquivo cadastro.html
    var idP = req.body.idPServer;
    var idA = req.body.idAServer;

    // Faça as validações dos valores
    if (idP == undefined) {
        res.status(400).send("Seu idP está undefined!");
    } else if (idA == undefined) {
        res.status(400).send("Seu idA está undefined!");
    } else {
        
        // Passe os valores como parâmetro e vá para o arquivo usuarioModel.js
        usuarioModel.atualizar(idP, idA)
            .then(
                function (resultado) {
                    res.json(resultado);
                }
            ).catch(
                function (erro) {
                    console.log(erro);
                    console.log(
                        "\nHouve um erro ao realizar o cadastro! Erro: ",
                        erro.sqlMessage
                    );
                    res.status(500).json(erro.sqlMessage);
                }
            );
    }
}

module.exports = {
    entrar,
    cadastrar,
    listar,
    testar,
    cadastrarP,
    atualizar
}
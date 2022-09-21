var database = require("../database/config");

function buscarUltimasMedidas(fkVoto, limite_linhas) {
    
    instrucaoSql = ''
    
    if (process.env.AMBIENTE_PROCESSO == "producao") {
        instrucaoSql = `select top ${limite_linhas}
                        temperatura, 
                        umidade, 
                        momento,
                        CONVERT(varchar, momento, 108) as momento_grafico
                    from medida
                    where fk_aquario = ${idAquario}
                    order by id desc`;

    } else if (process.env.AMBIENTE_PROCESSO == "desenvolvimento") {
        instrucaoSql = `select votos.voto, count(usuario.id) qtd_pessoas from usuario join votos on usuario.fkVoto = votos.id group by votos.voto;`;

    } /* else  if (process.env.AMBIENTE_PROCESSO == "desenvolvimento") {
        instrucaoSql = `select votos.voto, count(usuario.id) from usuario join votos on usuario.fkVoto = votos.id group by votos.voto;` */
     else { 

        console.log("\nO AMBIENTE (produção OU desenvolvimento) NÃO FOI DEFINIDO EM app.js\n");
        return
    }
    
    console.log("Executando a instrução SQL: \n" + instrucaoSql);
    return database.executar(instrucaoSql);
}

function buscarMedidasEmTempoReal(fkVoto) {
    
    instrucaoSql = ''
    
    if (process.env.AMBIENTE_PROCESSO == "producao") {       
        instrucaoSql = `select top 1
                        temperatura, 
                        umidade, CONVERT(varchar, momento, 108) as momento_grafico, 
                        fk_aquario 
                        from medida where fk_aquario = ${idAquario} 
                    order by id desc`;
        
    } else if (process.env.AMBIENTE_PROCESSO == "desenvolvimento") {
        instrucaoSql = `select votos.voto, count(usuario.id) qtd_pessoas from usuario join votos on usuario.fkVoto = votos.id group by votos.voto;`;

    } /* else  if (process.env.AMBIENTE_PROCESSO == "desenvolvimento") {
        instrucaoSql = `select votos (voto), count(usuario.id) from usuario join votos on usuario.fkVoto = votos.id group by votos.voto;` */
     else {
        console.log("\nO AMBIENTE (produção OU desenvolvimento) NÃO FOI DEFINIDO EM app.js\n");
        return
    }

    console.log("Executando a instrução SQL: \n" + instrucaoSql);
    return database.executar(instrucaoSql);
}


module.exports = {
    buscarUltimasMedidas,
    buscarMedidasEmTempoReal
}

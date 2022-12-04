

function buscarTemperatura(fkTorre) {
    
    instrucaoSql = ''
    
    instrucaoSql = `select top 7 Leitura as 'Temperatura' from Leitura where fkTorre = ${fkTorre} and fkComponente = 22 ORDER BY idLeitura DESC`;
        
    console.log("Executando a instrução SQL: \n" + instrucaoSql);
    return database.executar(instrucaoSql);
}

function buscarPlacaMae(fkTorre) {
    
    instrucaoSql = ''
    
    instrucaoSql = `select top 7 Leitura as 'Placa Mãe' from Leitura where fkTorre = ${fkTorre} and fkComponente = 23 ORDER BY idLeitura DESC`;
        
    console.log("Executando a instrução SQL: \n" + instrucaoSql);
    return database.executar(instrucaoSql);
}

function buscarDesempenho(fkTorre) {
    
    instrucaoSql = ''
    
    instrucaoSql = `select top 7 Leitura as 'Desempenho' from Leitura where fkTorre = ${fkTorre} and fkComponente = 24 ORDER BY idLeitura DESC`;
        
    console.log("Executando a instrução SQL: \n" + instrucaoSql);
    return database.executar(instrucaoSql);
}

module.exports = {
    buscarTemperatura,
    buscarPlacaMae,
    buscarDesempenho
}

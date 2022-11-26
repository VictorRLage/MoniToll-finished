package Repositorio

import Dominio.Leitura
import Dominio.Torre
import org.springframework.jdbc.core.JdbcTemplate

class LeituraRepositorio(val jdbcTemplate: JdbcTemplate)  {
    fun insertLeitura(leitura: Leitura){
        jdbcTemplate.update("INSERT INTO Leitura (Leitura, DataHora, fkTorre, fkComponente) VALUES (?, ?, ?, ?);",
            leitura.Leitura, leitura.DataHora, leitura.fkTorre, leitura.fkComponentes
        )
    }
}
package Config

import org.apache.commons.dbcp2.BasicDataSource
import org.springframework.jdbc.core.JdbcTemplate

class Conexao {
    fun getJdbcTemplate(): JdbcTemplate {
        val dataSource = BasicDataSource();
        dataSource.driverClassName = "com.microsoft.sqlserver.jdbc.SQLServerDriver"
        dataSource.url = "jdbc:sqlserver://montioll.database.windows.net;databaseName=Monitoll"
        dataSource.username = "Monitoll"
        dataSource.password = "Grupo7@123"

        val jdbcTemplate = JdbcTemplate(dataSource)
        return jdbcTemplate
    }
}
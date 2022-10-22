package Dominio

data class Usuario(var email:String, var senha:String, var fkEmpresa:Int) {
    constructor() : this("", "", 0)
}
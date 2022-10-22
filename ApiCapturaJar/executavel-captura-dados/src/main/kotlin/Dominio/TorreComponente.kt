package Dominio

data class TorreComponente(var fkTorre:Int, var fkComponentes:Int) {
    constructor() : this(0,0)
}
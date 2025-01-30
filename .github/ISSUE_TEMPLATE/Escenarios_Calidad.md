---
name: Escenario de Calidad
about: Crear un escenario de calidad
title: "[SEC] "
labels: ASR
assignees: ''
---
<table>
    <tbody>
        <tr>
            <td >ID</td>
            <td colspan=3>HUA-11</td>
        </tr>
        <tr>
            <td>Nombre</td>
            <td colspan=3>Notificación eventos adversos en los entrenamientos</td>
        </tr>
        <tr>
            <td>Descripción</td>
            <td colspan=3 >
Como administrador del sistema, cuando falle el componente de notificaciones dado que existe un alto volumen de usuarios conectados simultaneamente quiero que se active automaticamente un nodo de respaldo de este componente para que continue emitiendo estas notificaciones. Esto debe suceder en menos de 10 seg.
          </td>
        </tr>
        <tr>
            <td>Fuente</td>
            <td>Estímulo</td>
            <td>Artefacto</td>
            <td>Ambiente</td>
        </tr>
        <tr>
            <td>Deportista</td>
            <td>Evento adverso cerca al lugar donde se desarrolla un evento deportivo </td>
            <td>Componente Comunicaciones</td>
            <td>Operación Alta</td>
        </tr>
        <tr>
            <td colspan=2>Respuesta</td>
            <td colspan=2>Informe de este evento mediante una notificación</td>
        </tr>
        <tr>
            <td colspan=2>Medida de la respuesta</td>
            <td colspan=2>En menos de 10 segundos desde que el componente falló</td>
        </tr>
    </tbody>
</table>

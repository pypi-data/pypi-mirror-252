import{MenuController}from"../menu.mjs";class NewFileController extends MenuController{static menuName="New";static menuIcon="fa-solid fa-file";static menuShortcut="n";async onClick(){await this.application.resetState(),this.notify("info","Success","Successfully reset to defaults.")}}export{NewFileController as MenuController};

import{MenuController}from"../menu.mjs";class WikiController extends MenuController{static helpLink="https://github.com/painebenjamin/app.enfugue.ai/wiki";static menuName="Wiki";static menuIcon="fa-solid fa-book";static menuShortcut="w";async onClick(){window.open(this.constructor.helpLink)}}export{WikiController as MenuController};

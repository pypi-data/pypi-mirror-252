import{MenuController}from"../menu.mjs";class RegionPromptController extends MenuController{static menuName="Region Prompt";static menuIcon="fa-solid fa-text-width";async onClick(){this.canvas.addPromptNode()}}export{RegionPromptController as ToolbarController};

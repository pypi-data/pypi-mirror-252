import{FormView}from"../base.mjs";import{SelectInputView}from"../input.mjs";class IPAdapterFormView extends FormView{static fieldSets={"IP Adapter":{ipAdapterModel:{label:"Model",class:SelectInputView,config:{value:"default",options:{default:"Default",plus:"Plus","plus-face":"Plus Face","full-face":"Full Face"},tooltip:"Which IP adapter model to use. 'Plus' will in general find more detail in the source image while considerably adjusting the impact of your prompt, and 'Plus Face' will ignore much of the image except for facial features. 'Full Face' is similar to 'Plus Face' but extracts more features."}}}};static autoSubmit=!0}export{IPAdapterFormView};

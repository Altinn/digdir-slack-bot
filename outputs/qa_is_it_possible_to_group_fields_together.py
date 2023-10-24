user_input: is it possible to group fields together?
Response:
ExtractedSearchTerms(searchTerms=['group', 'fields', 'together'])
ExtractedSearchTerms(searchTerms=['group', 'fields', 'together'])
Unique URLs
[ 'https://docs.altinn.studio/app/development/ux/fields/grouping/panel/',
  'https://docs.altinn.studio/app/development/ux/fields/grouping/repeating/multipage/',
  'https://docs.altinn.studio/app/development/ux/fields/grouping/repeating/',
  'https://docs.altinn.studio/app/development/logic/validation/']
html_to_md docs:
[ { 'file_path': '/var/folders/01/_86bbblx2hj_1_w6b8wpn9jm0000gn/T/tmpp0dwjyjk/__docs.altinn.studio_app_development_ux_fields_grouping_panel_.md',
    'markdown': 'Group displayed as panel\n'
                '========================\n'
                '\n'
                'Configuration details for groups displayed as panels, and '
                'referencing group values in a panel\n'
                '\n'
                'Display group as part of Panel\n'
                '------------------------------\n'
                '\n'
                'On a Group component, the parameter `panel` can be set up.\n'
                'This says that the group should be displayed as part of the '
                '[Panel component](../../../components/panel).\n'
                '\n'
                'Here, you will recognize the appearance and settings that can '
                'be set on the panel component. Example configuration:\n'
                '\n'
                '\n'
                '```\n'
                '{\n'
                ' "id": "input-panel-group",\n'
                ' "type": "Group",\n'
                ' "children": [\n'
                ' "child1",\n'
                ' "child2"\n'
                ' ],\n'
                ' "dataModelBindings": {},\n'
                ' "textResourceBindings": {\n'
                ' "title": "This is just a demo of input panel outside of '
                'repeating group",\n'
                ' "body": "Here I just see that things work as expected."\n'
                ' },\n'
                ' "panel": {\n'
                ' "variant": "info"\n'
                ' }\n'
                '}\n'
                '\n'
                '```\n'
                'Here the group has been set up to be displayed as a panel '
                'with the variant “info”. The setup is otherwise exactly the '
                'same as a regular group.\n'
                '\n'
                'This will give the following output:\n'
                '\n'
                '[![Group with panel](input-panel.jpeg "Group with '
                'panel")](input-panel.jpeg)*Group with panel*It is possible to '
                'configure the following settings in the `panel` field of a '
                'group:\n'
                '\n'
                '\n'
                '\n'
                '| Parameter | Required | Description |\n'
                '| --- | --- | --- |\n'
                '| variant | Yes | Which variant of panel the group should be '
                'placed in. Available values are “info”, “success” and '
                '“warning” |\n'
                '| iconUrl | No | If you want your own icon as part of a '
                'panel, this can be set. Relative or full path, e.g. '
                '“awesomeIcon.png” or '
                '“[http://cdn.example.com/awesomeIcon.png"](http://cdn.example.com/awesomeIcon.png%22) '
                '|\n'
                '| iconAlt | No | Alternate text for the custom icon. Can only '
                'be set if iconUrl has been set. Can be plain text or a '
                'reference to a text resource. |\n'
                '| groupReference | No | Reference to a different (repeating) '
                'group. Can be used if you wish to add elements to a repeating '
                'group from some other context. [Read '
                'more.](#add-element-from-separate-repeating-group) |\n'
                '\n'
                'Example:\n'
                '\n'
                '\n'
                '```\n'
                '{\n'
                ' "id": "input-panel-group",\n'
                ' "type": "Group",\n'
                ' "panel": {\n'
                ' "variant": "info",\n'
                ' "iconUrl": "kort.svg",\n'
                ' "iconAlt": "Betalingskort ikon"\n'
                ' }\n'
                '}\n'
                '\n'
                '```\n'
                '### Add element from separate repeating group\n'
                '\n'
                'A use case one can imagine is that the user is asked to '
                'choose from an already filled out repeating group. One '
                'possible case is that the user is registering a set of '
                'suspicious transactions.\n'
                'Here, the user first enters a set of separate payment cards '
                'as a repeating group. Later on in the form, the user will '
                'choose elements from this group when adding a suspicious '
                'transaction.\n'
                'While filling out the suspicious transaction, the user '
                'remembers that they forgot to add a payment card, but do not '
                'wish to navigate all the way back to the original payment '
                'card group.\n'
                '\n'
                'This is where the `groupReference` parameter comes in handy. '
                'This will open up for the possibility to add an element to a '
                'repeating group from the context from which you are using '
                'this list.\n'
                '\n'
                'A picture to illustrate the use case:\n'
                '\n'
                '[![GroupReference case](panel-reference-case.png '
                '"GroupReference '
                'case")](panel-reference-case.png)*GroupReference case*In this '
                'fictitious case the groups are placed directly above each '
                'other, but imagine that these are filled out on different '
                'pages in the form.\n'
                'To achieve this setup, a group of elements are added to the '
                'repeating group that is set up with transactions (group-2) '
                'with a reference to the first group with payment cards '
                '(group-1).\n'
                'The following group component is one of the children of '
                'group-2:\n'
                '\n'
                '\n'
                '```\n'
                '{\n'
                ' "id": "input-panel-group",\n'
                ' "type": "Group",\n'
                ' "maxCount": 3,\n'
                ' "dataModelBindings": {\n'
                ' "group": "Payment.Cards"\n'
                ' },\n'
                ' "textResourceBindings": {\n'
                ' "title": "Legg til nytt betalingskort",\n'
                ' "body": "Kortet du registrer vil bli lagret og tilgjengelig '
                'i resten av tjenesten.",\n'
                ' "add\\_label": "Legg til nytt betalingskort"\n'
                ' },\n'
                ' "panel": {\n'
                ' "showIcon": true,\n'
                ' "iconUrl": "kort.svg",\n'
                ' "variant": "success",\n'
                ' "groupReference": {\n'
                ' "group": "first-group"\n'
                ' }\n'
                ' }\n'
                '}\n'
                '\n'
                '```\n'
                'The text resources that can be set are:\n'
                '\n'
                '* `title` - panel title\n'
                '* `body` - panel body. Placed above the group elements.\n'
                '* `add_label` - text for the “add new”-button.\n'
                '\n'
                'If `children` is not set on the group, the children of the '
                'referenced group will be rendered.\n'
                'By adding to `children` you can freely define that only a '
                'subset of all children of the referenced group should be '
                'displayed.\n'
                '\n'
                'Demonstration:\n'
                '\n'
                '[![Demonstration of groupReference](panel-reference-demo.gif '
                '"Demonstration of '
                'groupReference")](panel-reference-demo.gif)*Demonstration of '
                'groupReference*See [example '
                'app](https://altinn.studio/repos/ttd/input-panel-demo) for '
                'complete setup in form layout.\n'
                '\n',
    'url': 'https://docs.altinn.studio/app/development/ux/fields/grouping/panel/'},
  { 'file_path': '/var/folders/01/_86bbblx2hj_1_w6b8wpn9jm0000gn/T/tmpp0dwjyjk/__docs.altinn.studio_app_development_ux_fields_grouping_repeating_multipage_.md',
    'markdown': 'Multiple pages within a group\n'
                '=============================\n'
                '\n'
                'How to show components in a group in multiple pages\n'
                '\n'
                'Multiple pages within group-display\n'
                '-----------------------------------\n'
                '\n'
                'This functionality is as of today only available for '
                'repeating groups. Displaying of groups over\n'
                'multiple pages inside the editing area of the group is only '
                'supported for groups at the top level, and is not supported\n'
                'for nested groups.When entering data in a group, there may be '
                'incidents where each element in the group contains multiple '
                'fields, which may result in a lot of scrolling\n'
                'and confusion for the user. To solve this, there has been '
                'implemented a possibility to split the fill out over multiple '
                'pages, which the user can navigate\n'
                'through while filling out the group element. The navigation '
                'takes place within a layout, and updates\n'
                'only the display within the editing area of the group.\n'
                '\n'
                'To make use of this functionality, you will have to *prefix* '
                'the components in the `children` list with a number '
                'indicating which “page” of the fill out\n'
                'the component should be displayed on, followed by `:`. We '
                'start the count on `0`, that is to say components to be '
                'displayed on the first “page” must be prefixed with\n'
                '`0:`. Components to be displayed on the second page must be '
                'prefixed with `1:`, and so on. In addition, you must set '
                '`"multiPage": true` in the `edit`-parameter.\n'
                'See example below:\n'
                '\n'
                '\n'
                '```\n'
                '{\n'
                ' "id": "Some-group-id",\n'
                ' "type": "Group",\n'
                ' "children": [\n'
                ' "0:fnr",\n'
                ' "1:fornavn",\n'
                ' "1:mellomnavn",\n'
                ' "1:etternavn"\n'
                ' ],\n'
                ' "maxCount": 10,\n'
                ' "dataModelBindings": {\n'
                ' "group": "familie.barn"\n'
                ' },\n'
                ' "edit": {\n'
                ' "multiPage": true,\n'
                ' "mode": "hideTable",\n'
                ' }\n'
                '}\n'
                '\n'
                '```\n'
                'Here a [mode](../edit#mode) that hides the table when editing '
                'has also been added.\n'
                'The result will be as displayed below.\n'
                '\n'
                '[![Fill-out of group over multiple '
                '&ldquo;pages&rdquo;](group-multipage.gif "Fill-out of group '
                'over multiple pages")](group-multipage.gif)*Fill-out of group '
                'over multiple pages*',
    'url': 'https://docs.altinn.studio/app/development/ux/fields/grouping/repeating/multipage/'},
  { 'file_path': '/var/folders/01/_86bbblx2hj_1_w6b8wpn9jm0000gn/T/tmpp0dwjyjk/__docs.altinn.studio_app_development_ux_fields_grouping_repeating_.md',
    'markdown': 'Repeating groups\n'
                '================\n'
                '\n'
                'Setup for repeating groups\n'
                '\n'
                'Groups in the data model contain one or more fields. Groups '
                'are defined as *repeating* if they have `maxCount > 1` in\n'
                'the layout configuration. A group that is repeating in the '
                'data model must also be set up as repeating in the form, if\n'
                'not, data saving will fail. In JSON, a repeating group is '
                'defined as an array of objects, where each object is a '
                'group.\n'
                'In XML, a repeating group is defined as a list of elements, '
                'where each element is a group/object with properties.\n'
                '\n'
                'Example\n'
                '-------\n'
                '\n'
                'Below is a form with a repeating group that:\n'
                '\n'
                '* Contains two components (checkbox and address)\n'
                '* Can be repeated up to three times\n'
                '* Is bound to the data model group/array `GruppeListe`\n'
                '\n'
                '[![Form with repeating group](repeating-groups-demo.gif "Form '
                'with repeating group")](repeating-groups-demo.gif)*Form with '
                'repeating group*[*Vis/skjul innhold*\n'
                'Show configuration for this '
                'screenshot](#expandable-full-example)\n'
                '```\n'
                ' 1[\n'
                ' 2 {\n'
                ' 3 "id": "gruppe",\n'
                ' 4 "type": "Group",\n'
                ' 5 "children": [\n'
                ' 6 "avkrysningsboks",\n'
                ' 7 "adresse"\n'
                ' 8 ],\n'
                ' 9 "maxCount": 3,\n'
                '10 "dataModelBindings": {\n'
                '11 "group": "GruppeListe"\n'
                '12 }\n'
                '13 },\n'
                '14 {\n'
                '15 "id": "avkrysningsboks",\n'
                '16 "type": "Checkboxes",\n'
                '17 "textResourceBindings": {\n'
                '18 "title": "Avkrysningsboks"\n'
                '19 },\n'
                '20 "dataModelBindings": {\n'
                '21 "simpleBinding": "GruppeListe.Avkrysning"\n'
                '22 },\n'
                '23 "options": [\n'
                '24 {\n'
                '25 "label": "Navn",\n'
                '26 "value": "Verdi1"\n'
                '27 },\n'
                '28 {\n'
                '29 "label": "Adresse",\n'
                '30 "value": "Verdi2"\n'
                '31 }\n'
                '32 ],\n'
                '33 "required": true\n'
                '34 },\n'
                '35 {\n'
                '36 "id": "addresse",\n'
                '37 "type": "AddressComponent",\n'
                '38 "textResourceBindings": {\n'
                '39 "title": "Adresse" \n'
                '40 },\n'
                '41 "dataModelBindings": {\n'
                '42 "address": "GruppeListe.Adresse",\n'
                '43 "zipCode": "GruppeListe.Postnr",\n'
                '44 "postPlace": "GruppeListe.Poststed"\n'
                '45 },\n'
                '46 "simplified": true,\n'
                '47 "readOnly": false,\n'
                '48 "required": true\n'
                '49 }\n'
                '50]\n'
                '\n'
                '```\n'
                'Parameters\n'
                '----------\n'
                '\n'
                '\n'
                '\n'
                '| Parameter | Required | Description |\n'
                '| --- | --- | --- |\n'
                '| id | Yes | Unique ID, same as ID on other components. Must '
                'be unique in the layout file, and should be unique across '
                'pages. |\n'
                '| type | Yes | Must be ‘Group’ |\n'
                '| dataModelBindings | No | Must be set for repeating groups '
                'with form components inside. Should point to the repeating '
                'group in the data model. |\n'
                '| [textResourceBindings](#textresourcebindings) | No | Can be '
                'set for repeating groups, see '
                '[description](#textresourcebindings). |\n'
                '| maxCount | Yes | The number of times a group can repeat. '
                'Must be set to `1` or more for the group component to work as '
                'a repeating group. |\n'
                '| minCount | No | Validation. The minimum number of times a '
                'group must repeat before the user can submit the form. |\n'
                '| children | Yes | List of the component IDs that are to be '
                'included in the repeating group. |\n'
                '| <edit> | No | Options for how to display the group when '
                'editing a row. |\n'
                '| tableHeaders | No | List of components that are to be '
                'included as part of the table header fields. If not '
                'specified, all components are displayed. |\n'
                '| '
                '[tableColumns](table/#widths-alignment-and-overflow-for-columns) '
                '| No | Object containing column options for specified '
                'headers. If not specified, all columns will use default '
                'display settings. |\n'
                '\n'
                'textResourceBindings\n'
                '--------------------\n'
                '\n'
                'It is possible to add different keys in textResourceBindings '
                'to overrule default texts.\n'
                '\n'
                '* `title` - title to show above the group row in a [Summary '
                'component](../../../pages/summary).\n'
                '* `add_button` - is added at the end of the “Add new” text on '
                'the button, and can be used to e.g. get text that says “Add '
                'new person”.\n'
                '* `add_button_full` - is used as custom text on the “Add new” '
                'button. Overrides `add_button` if both are set.\n'
                '* `save_button` - is used as text on the “Save” button when '
                'the user is filling out data.\n'
                '* `save_and_next_button` - is used as text on the “Save and '
                'open next” button if enabled.\n'
                '* `edit_button_open` - is used as text on the “Edit” button '
                'on the table when the user is opening an element.\n'
                '* `edit_button_close` - is used as text on the “Edit” button '
                'on the table when the user is closing an element.\n'
                '* [Row editing '
                'settings](/app/development/ux/fields/grouping/repeating/edit/)Change '
                'how to edit/fill out a row in a repeating group\n'
                '* [Table '
                'configuration](/app/development/ux/fields/grouping/repeating/table/)Configuration '
                'for the table that is shown above repeating groups\n'
                '* [Attachments in repeating '
                'groups](/app/development/ux/fields/grouping/repeating/attachments/)Specifics '
                'on how to set up attachment uploading in repeating groups\n'
                '* [Dynamic behaviour in repeating '
                'groups](/app/development/ux/fields/grouping/repeating/dynamics/)How '
                'to hide rows in a repeating group\n'
                '* [Multiple pages within a '
                'group](/app/development/ux/fields/grouping/repeating/multipage/)How '
                'to show components in a group in multiple pages\n'
                '\n',
    'url': 'https://docs.altinn.studio/app/development/ux/fields/grouping/repeating/'},
  { 'file_path': '/var/folders/01/_86bbblx2hj_1_w6b8wpn9jm0000gn/T/tmpp0dwjyjk/__docs.altinn.studio_app_development_logic_validation_.md',
    'markdown': 'Validation\n'
                '==========\n'
                '\n'
                'How to add logic to validate form data?\n'
                '\n'
                'On this page:\n'
                '-------------\n'
                '\n'
                '* [Introduction](#introduction)\n'
                '* [Client-side validation](#client-side-validation)\n'
                '* [Server-side validation](#server-side-validation)\n'
                '* [How to add custom '
                'validation](#how-to-add-custom-validation)\n'
                '* [Single field validation](#single-field-validation)\n'
                '* [Soft validations](#soft-validations)\n'
                '* [Group validation](#group-validation)\n'
                'Introduction\n'
                '------------\n'
                '\n'
                'Validations ensures that the user’s input is valid with '
                'regard to the data model,\n'
                'in addition to all custom rules that are set up for the '
                'application.\n'
                'Validations can be run either on the client- (the browser) or '
                'the server-side.\n'
                '\n'
                'Validations can also be set up to [trigger on page '
                'navigation](/app/development/ux/pages/navigation/#validation-on-page-navigation).\n'
                '\n'
                'Client-side validation\n'
                '----------------------\n'
                '\n'
                'This is validation that is run in the browser, before data is '
                'sent to server for saving. This makes it possible to give '
                'quick feedback to\n'
                'the user during the process of filling out the form.\n'
                '\n'
                'Client-side validation is based on the data model of the '
                'form, and uses this to determine what is valid input in a\n'
                'field.\n'
                'Specifically, the JSON schema version of the data model is '
                'used for validation. This is automatically generated when\n'
                'uploading an XSD.\n'
                'It is possible to make changes in the JSON schema file '
                'directly to adapt the validation when needed.\n'
                '\n'
                '**Note that if you make changes in the JSON schema manually, '
                'and then update the XSD and re-upload it, a new\n'
                'JSON schema will also be generated and all manual adaptations '
                'will have to be remade. It is therefore recommended to\n'
                'make changes in the XSD and/or the data modeling tool\n'
                'for these changes to be reflected in the JSON schema.**\n'
                '\n'
                'An example of how a field can be defined in the JSON schema '
                'data model is:\n'
                '\n'
                '\n'
                '```\n'
                '"someField": {\n'
                ' "type": "string",\n'
                ' "maxLength": "4"\n'
                '}\n'
                '\n'
                '```\n'
                'Input in this field will be validated towards the limits that '
                'are set, and an error message will appear if these are not '
                'met - in this case, if\n'
                'input is a text longer than four characters.\n'
                '\n'
                '### Default error messages\n'
                '\n'
                'Default error messages has been set up for all validations '
                'done on the client-side. See the overview below.\n'
                '\n'
                '\n'
                '\n'
                '| Rule | Error message bokmål | Error message nynorsk | Error '
                'message english |\n'
                '| --- | --- | --- | --- |\n'
                '| min | ‘Minste gyldig verdi er {0}’ | ‘Minste gyldig verdi '
                'er {0}’ | ‘Minimum valid value is {0}’ |\n'
                '| max | ‘Største gyldig verdi er {0}’ | ‘Største gyldig verdi '
                'er {0}’ | ‘Maximum valid value is {0}’ |\n'
                '| minLength | ‘Bruk {0} eller flere tegn’ | ‘Bruk {0} eller '
                'flere tegn’ | ‘Use {0} or more characters’ |\n'
                '| maxLength | ‘Bruk {0} eller færre tegn’ | ‘Bruk {0} eller '
                'færre tegn’ | ‘Use {0} or fewer characters’ |\n'
                '| length | ‘Antall tillatte tegn er {0}’ | ‘Antall tillatte '
                'tegn er {0}’ | ‘Number of characters allowed is {0}’ |\n'
                '| pattern | ‘Feil format eller verdi’ | ‘Feil format eller '
                'verdi’ | ‘Wrong format or value’ |\n'
                '| required | ‘Du må fylle ut {0}’ | ‘Du må fylle ut {0}’ | '
                '‘You have to fill out {0}’ |\n'
                '| enum | ‘Kun verdiene {0} er tillatt’ | ‘Kun verdiene {0} er '
                'tillatt’ | ‘Only the values {0} are permitted’ |\n'
                '\n'
                '### More about error messages for required fields\n'
                '\n'
                'For a smoother user experience, error messages for missing '
                'data in required fields won’t be displayed automatically\n'
                'while filling out a form, unless validation is triggered [for '
                'a single field](#single-field-validation), when saving\n'
                'a [row in a repeating group](#group-validation) or\n'
                '[when navigating to another '
                'page](/app/development/ux/pages/navigation/#validation-on-page-navigation).\n'
                '\n'
                'The error message for required fields is as defined above, '
                '*“You have to fill out {0}”*. The `{0}` symbol is replaced '
                'with the field that\n'
                'the error message is shown for. This is done in the following '
                'way:\n'
                '\n'
                '* If `shortName` text is defined for the component, this is '
                'used. *This is a new text that is currently used only for '
                'this specific error message.*\n'
                '* If the `shortName` text is not defined, the `title` text '
                'for the component is used - this is the components label '
                'text. The text will be converted to use a lowercase letter '
                'first, unless the text looks like an acronym.\n'
                '* In some special cases (Address component) where there are '
                'multiple fields within the component, the default labels for '
                'the fields is used.\n'
                '\n'
                '#### Example: Component with only `title`\n'
                '\n'
                '\n'
                '```\n'
                '{\n'
                ' "id": "firstName",\n'
                ' "type": "Input",\n'
                ' "textResourceBindings": {\n'
                ' "title": "text-firstName"\n'
                ' },\n'
                ' ... //etc\n'
                '}\n'
                '\n'
                '```\n'
                'With resource texts:\n'
                '\n'
                '\n'
                '```\n'
                '...\n'
                '{\n'
                ' "id": "text-firstName",\n'
                ' "value": "First name"\n'
                '}\n'
                '\n'
                '```\n'
                'The error message would then be `"You have to fill out First '
                'name"`.\n'
                '\n'
                '#### Example: Component with `shortName`\n'
                '\n'
                'If the field’s prompt is long or not suitable for use in the '
                'validation message, you can add a `shortName` text that can '
                'be used instead.\n'
                '*Note that this only applies to this specific validation '
                'message - the `shortName` text is not used otherwise in the '
                'solution as of now.*\n'
                '\n'
                '\n'
                '```\n'
                '{\n'
                ' "id": "firstName",\n'
                ' "type": "Input",\n'
                ' "textResourceBindings": {\n'
                ' "title": "text-firstName",\n'
                ' "shortName": "firstName-short",\n'
                ' },\n'
                ' ... //etc\n'
                '}\n'
                '\n'
                '```\n'
                'With resource texts:\n'
                '\n'
                '\n'
                '```\n'
                '...\n'
                '{\n'
                ' "id": "text-firstName",\n'
                ' "value": "Please type your first name in the field below:"\n'
                '},\n'
                '{\n'
                ' "id": "firstName-short",\n'
                ' "value": "your first name"\n'
                '}\n'
                '\n'
                '```\n'
                'The error message would then be `"You have to fill out your '
                'first name"`.\n'
                '\n'
                '### Custom error messages\n'
                '\n'
                'It is possible to define custom error messages that will be '
                'displayed when a field doesn’t pass the validation check. '
                'This is done by including a parameter `errorMessage` where '
                'the field is defined in the JSON schema.\n'
                'The JSON schema file is in the folder `App/models` and has a '
                'naming patterns as follows; `*.schema.json`,\n'
                '\n'
                'An example of how to extend the example previously presented '
                'with a custom error message:\n'
                '\n'
                '\n'
                '```\n'
                '"someField": {\n'
                ' "type": "string",\n'
                ' "maxLength": "4",\n'
                ' "errorMessage": "myCustomError"\n'
                '}\n'
                '\n'
                '```\n'
                'The error text can be included directly. To enable language '
                'support, add a text key for a [text defined in the resource '
                'files](../../ux/texts).\n'
                '\n'
                'Notice that if you have a reference to a definition the error '
                'message must be added to the `property`-field and not the '
                'reference/definition.\n'
                'Example:\n'
                '\n'
                '\n'
                '```\n'
                '{\n'
                ' "properties": {\n'
                ' "person": {\n'
                ' "$ref" : "#/definitions/personDefinition",\n'
                ' "errorMessage": "myCustomError",\n'
                ' }\n'
                ' },\n'
                ' "definitions": {\n'
                ' "personDefinition" : {\n'
                ' "age": {\n'
                ' "type": "number"\n'
                ' },\n'
                ' ...\n'
                ' }\n'
                '}\n'
                '\n'
                '```\n'
                'Note that when the XSD is changed, the custom error messages '
                'will de removed from the JSON schema.\n'
                'In the future, there will be support for setting custom error '
                'messages in the data modelling tool in Altinn Studio. But for '
                'now, this is a manual job.Server-side validation\n'
                '----------------------\n'
                '\n'
                'Server-side validation can be split into two categories:\n'
                '\n'
                '* **Validations against data model** - These run '
                'automatically whenever the user attempts to submit form '
                'data.\n'
                '* **Custom validations** - these are written by the '
                'application developer,\n'
                'and run when the user attempts to submit form data or move '
                'the process to a new step.\n'
                '\n'
                'How to add custom validation\n'
                '----------------------------\n'
                '\n'
                'Custom validation can also be split into two categories; '
                'task-validation and data-validation.\n'
                '\n'
                '* Task-validation will run each time validation is triggered '
                'either manually from the application or when you attempt to '
                'move forward in the process.\n'
                '* Data-validation will run if you’re on a step that has '
                'defined data elements associated with it.\n'
                '\n'
                'Validations are written i C# and depending on the version of '
                'the application template and Nuget packages you are using,\n'
                'the way the implementation is done varies slightly. In the '
                'earlier versions it’s a pre-created file where you put your\n'
                'logic, while from version 7 and onwards you implement an '
                'interface in whatever class you like. The interface happens '
                'to\n'
                'be equal to the pre-defined class in the earlier versions. '
                'The examples below which referrers to the methods to add '
                'your\n'
                'validation logic to is the same.\n'
                '\n'
                '\n'
                'v7In version 7 the way to do custom code instantiation has '
                'changed. We now use an dependency injection based approach\n'
                'instead of overriding methods. If you previously used to '
                'place your custom code in the *ValidateData* and '
                '*ValidateTask*\n'
                'methods in the *ValidationHandler.cs* class you will see that '
                'it’s mostly the same.\n'
                '\n'
                '1. Create a class that implements the `IInstanceValidator` '
                'interface found in the `Altinn.App.Core.Features.Validation` '
                'namespace.  \n'
                'You can name and place the file in any folder you like within '
                'your project, but we suggest you use meaningful namespaces '
                'like in any other .Net project.\n'
                '2. Register you custom implementation in the *Program.cs* '
                'class\n'
                '```\n'
                'services.AddTransient<IInstanceValidator, '
                'InstanceValidator>();\n'
                '\n'
                '```\n'
                'This ensures your custom code is known to the application and '
                'that it will be executed.\n'
                'v4, v5, v6\n'
                'Validations should be added to the '
                '`ValidationHandler.cs`-file in the application template.\n'
                'The file can be accessed and edited in Altinn Studio through '
                'the logic menu, by selecting *Rediger valideringer*,\n'
                'or directly in the application repo where the file is under '
                'the `logic/Validation`-folder.From here on the examples '
                'should be valid for all versions:)\n'
                '\n'
                'Custom logic are added to the `ValidateData` and '
                '`ValidateTask`-methods.\n'
                'The former takes in a data object and the latter takes in the '
                'instance and taskId.\n'
                'To add a validation error, the `AddModelError`-method of the '
                '`validationResult`-object, which is a parameter in both '
                'methods, is used.\n'
                '\n'
                'An example of a simple data validation that tests that the '
                'field *FirstName* does not contain the value *1337*, when the '
                'root element of the model is `Skjema` is shown below:\n'
                '\n'
                '\n'
                '```\n'
                'public void ValidateData(object data, ModelStateDictionary '
                'validationResults)\n'
                '{\n'
                ' if (data.GetType() == typeof(Skjema))\n'
                ' {\n'
                ' // Cast instance data to model type\n'
                ' Skjema model = (Skjema)data;\n'
                '\n'
                ' // Get value to test - FirstName\n'
                ' string firstName = Skjema?.Person?.FirstName;\n'
                '\n'
                ' // Check if FirstName exists, and contains the value "1337"\n'
                ' if (firstName != null && firstName.Contains("1337"))\n'
                ' {\n'
                ' // Add validation error, with error message and list\n'
                ' // of affected fields (in this case Person.FirstName)\n'
                ' validationResults.AddModelError(\n'
                ' "Person.FirstName",\n'
                ' "Error: First name cannot contain the value \'1337\'."\n'
                ' );\n'
                ' }\n'
                ' }\n'
                '}\n'
                '\n'
                '```\n'
                'See comments in code above for an explanation of what the '
                'different parts do.\n'
                '\n'
                'In the other parameter of the method `AddModelError`, where '
                "it says “*Error: First name cannot contain the value '\n"
                '1337’*”, you can use a text key for a [text defined in the '
                'resource files](../../ux/texts) for multilingual support.\n'
                '\n'
                'An example of a simple task validation that checks how long '
                'the user spent on Task\\_1 and returns an error if there has '
                'gone more than three days:\n'
                '\n'
                '\n'
                '```\n'
                'public async Task ValidateTask(Instance instance, string '
                'taskId, ModelStateDictionary validationResults)\n'
                '{\n'
                ' if (taskId.Equals("Task\\_1"))\n'
                ' {\n'
                ' DateTime deadline = '
                '((DateTime)instance.Created).AddDays(3);\n'
                ' if (DateTime.UtcNow < deadline)\n'
                ' {\n'
                ' validationResults.AddModelError("Task\\_1", $"Completion of '
                'Task\\_1 has taken too long. Please start over.");\n'
                ' }\n'
                ' }\n'
                '}\n'
                '\n'
                '```\n'
                'Single field validation\n'
                '-----------------------\n'
                '\n'
                'If there is a need for immediate validation of a field\n'
                'that can not be covered in the client side validation,\n'
                'you can set up a trigger for validation on single fields in '
                '`formLayout.json`\n'
                '\n'
                '**NOTE**: Trigger for validation on single fields in '
                'Stateless apps is not currently supported.\n'
                '```\n'
                '{\n'
                ' "data": {\n'
                ' "layout": [\n'
                ' {\n'
                ' "id": "3611fb2a-c06b-4fa7-a400-3f6c1ece64e1",\n'
                ' "textResourceBindings": {\n'
                ' "title": '
                '"25795.OppgavegiverNavnPreutfyltdatadef25795.Label"\n'
                ' },\n'
                ' "dataModelBindings": {\n'
                ' "simpleBinding": "etatid"\n'
                ' },\n'
                ' "type": "Input",\n'
                ' "triggers": ["validation"] , // <--- Add this field\n'
                ' },\n'
                ' {\n'
                ' "id": "9ec368da-d6a9-4fbd-94d0-b4dfa8891981",\n'
                ' "type": "Button",\n'
                ' "textResourceBindings": {\n'
                ' "title": "Button"\n'
                ' },\n'
                ' "dataModelBindings": {},\n'
                ' "textResourceId": "Standard.Button.Button",\n'
                ' "customType": "Standard"\n'
                ' }\n'
                ' ]\n'
                ' }\n'
                '}\n'
                '\n'
                '```\n'
                'Note that if you define a field to trigger validation '
                'server-side, only the result of this validation will be '
                'displayed. Meaning,\n'
                'if there is another client-side validation defined, a '
                'possible server-side validation of the field will overwrite '
                'these. Therefore, you should make sure\n'
                'to implement all necessary validations on the server-side as '
                'well. It is possible to attach multiple error messages to the '
                'same field if needed.The configuration above will result in '
                'your own custom validation in `ValidationHandler.cs`\n'
                'being triggered each time the field is updated. If you need '
                'to know which field\n'
                'triggered the validation, this is available in the '
                'http-context as a header of the request named '
                '*ValidationTriggerField*.\n'
                '\n'
                'An example of a custom validation where the header value is '
                'retrieved is shown below.\n'
                '\n'
                '\n'
                '```\n'
                ' public async Task ValidateData(object data, '
                'ModelStateDictionary validationResults)\n'
                ' {\n'
                ' \\_httpContextAccessor.HttpContext\n'
                ' .Request.Headers\n'
                ' .TryGetValue("ValidationTriggerField", out StringValues '
                'triggerValues);\n'
                '\n'
                ' string triggerField = '
                'triggerValues.FirstOrDefault(string.Empty);\n'
                '\n'
                ' if (triggerField.Equals("kommune"))\n'
                ' {\n'
                ' // Cast instance data to model type\n'
                ' flyttemelding model = (flyttemelding)data;\n'
                '\n'
                ' // Get value to test - Kommune\n'
                ' string kommune = model.kommune;\n'
                '\n'
                ' if (!kommune.Equals("Oslo"))\n'
                ' {\n'
                ' validationResults.AddModelError(triggerField, "This is not a '
                'valid municipality.");\n'
                ' }\n'
                ' }\n'
                '\n'
                ' await Task.CompletedTask;\n'
                ' }\n'
                '\n'
                '```\n'
                '**NOTE** validation of single fields should be implemented in '
                'a way where it is both run on triggers and during general '
                'validation.\n'
                'The example that revolves multiple complex validations show '
                'how this can be implemented.\n'
                '\n'
                'Several things has been done to get this code to run\n'
                '\n'
                '1. In *ValidationHandler.cs* `using '
                'Microsoft.Extensions.Primitives;` is included at the top of '
                'the file to be able to use `StringValues`.\n'
                '2. In *App.cs* `using Microsoft.AspNetCore.Http;` is included '
                'at the top of the file to be able to use '
                '`IHttpContextAccessor`.\n'
                '3. In *App.cs* `IHttpContextAccessor` is dependency injected '
                'in the constructor and passed along to ValidationHandler.\n'
                '\n'
                '\n'
                '```\n'
                'public App(\n'
                ' IAppResources appResourcesService,\n'
                ' ILogger<App> logger,\n'
                ' IData dataService,\n'
                ' IProcess processService,\n'
                ' IPDF pdfService,\n'
                ' IProfile profileService,\n'
                ' IRegister registerService,\n'
                ' IPrefill prefillService,\n'
                ' IHttpContextAccessor httpContextAccessor // <--- Add this '
                'line\n'
                ' ) : base(appResourcesService, logger, dataService, '
                'processService, pdfService, prefillService)\n'
                ' {\n'
                ' \\_logger = logger;\n'
                ' \\_validationHandler = new '
                'ValidationHandler(httpContextAccessor); // <--- Include the '
                'new property here\n'
                ' \\_calculationHandler = new CalculationHandler();\n'
                ' \\_instantiationHandler = new '
                'InstantiationHandler(profileService, registerService);\n'
                ' }\n'
                '\n'
                '```\n'
                'If there are multiple complex validations that are time '
                'consuming, it is recommended to implement several private '
                'methods\n'
                'to validate these and use ValidationTriggerField to determine '
                'which private method is to be run.\n'
                'You can e.g. use a *switch statement* to accomplish this.\n'
                '\n'
                '\n'
                '```\n'
                'public async Task ValidateData(object data, '
                'ModelStateDictionary validationResults)\n'
                '{\n'
                ' if (data is flyttemelding model)\n'
                ' {\n'
                ' \\_httpContextAccessor.HttpContext\n'
                ' .Request.Headers\n'
                ' .TryGetValue("ValidationTriggerField", out StringValues '
                'triggerValues);\n'
                '\n'
                ' string triggerField = '
                'triggerValues.FirstOrDefault(string.Empty);\n'
                '\n'
                ' switch (triggerField)\n'
                ' {\n'
                ' case "kommune":\n'
                ' ValidateKommune(model, validationResults);\n'
                ' break;\n'
                ' case "boaddresse":\n'
                ' ValidateBoAdresse(model, validationResults);\n'
                ' break;\n'
                ' default:\n'
                ' ValidateKommune(model, validationResults);\n'
                ' ValidateBoAdresse(model, validationResults);\n'
                ' break;\n'
                ' }\n'
                ' }\n'
                '}\n'
                '\n'
                'private void ValidateKommune(flyttemelding model, '
                'ModelStateDictionary validationResults)\n'
                '{\n'
                ' if (model.kommune != null && !model.kommune.Equals("Oslo"))\n'
                ' {\n'
                ' validationResults.AddModelError(\n'
                ' nameof(model.kommune), \n'
                ' "This is not a valid municipality.");\n'
                ' }\n'
                '}\n'
                'private void ValidateBoAdresse(flyttemelding model, '
                'ModelStateDictionary validationResults)\n'
                '{\n'
                ' if (model.boaddresse != null && model.boaddresse.Length > '
                '150)\n'
                ' {\n'
                ' validationResults.AddModelError(\n'
                ' nameof(model.boaddresse), \n'
                ' "Address can not be longer than 150 characters.");\n'
                ' }\n'
                '}\n'
                '\n'
                '```\n'
                '### Specify that validation errors are fixed\n'
                '\n'
                'When validation is triggered by a single field, all former '
                'validations on this field will be removed pending a response '
                'from the last validation.\n'
                'If a field triggers validation that updates/adds an error '
                'message to multiple fields at once, these will not be removed '
                'even when there no longer are any\n'
                'errors in these fields. This is because there is no way to '
                'know which fields may have been validated through a single '
                'field validation.\n'
                '\n'
                'For example, if you have two fields; first name and last '
                'name. Both fields trigger single field validation, and if '
                'both fields have a value, you can validate that\n'
                'the full name can not be longer than 50 characters. An error '
                'message is then set on both fields. If you correct this by '
                'changing the first name, the error message from first name '
                'will\n'
                'disappear, but the error message on the last name field will '
                'still be displayed even though the validation does not set '
                'any error messages on the fields.\n'
                '\n'
                '\n'
                '```\n'
                'private void ValidateFullName(Datamodell model, '
                'ModelStateDictionary validationResults)\n'
                '{\n'
                ' if (!string.isNullOrEmpty(model.fornavn) && '
                '!string.isNullOrEmpty(model.etternavn)\n'
                ' && model.fornavn.Length + model.etternavn.Length > 50)\n'
                ' {\n'
                ' validationResults.addModelError(nameof(model.fornavn),\n'
                ' "Full name can not be longer than 50 characters.");\n'
                ' validationResults.addModelError(nameof(model.etternavn),\n'
                ' "Full name can not be longer than 50 characters.");\n'
                ' }\n'
                '}\n'
                '\n'
                '```\n'
                'To be able to remove old error messages in a case like this, '
                'there has been added support to be able to specify that a '
                'validation error has been **fixed**.\n'
                'Then, the field in question will be able to be notified that '
                'a specific error message that it is displaying has been fixed '
                'and can now be hidden.\n'
                '\n'
                'This is done by adding a validation error in the code in the '
                'case where there are no errors in the validation,\n'
                'and set `*FIXED*` in front of the error message itself. This '
                'corresponds to the setup for [soft '
                'validation](#soft-validations).\n'
                'This prefix causes the error message that is set to be '
                'removed from the field in question, or ignored (if there is '
                'no error message on the field already).\n'
                '\n'
                'You can now expand the example above to support this:\n'
                '\n'
                '\n'
                '```\n'
                'private void ValidateFullName(Datamodell model, '
                'ModelStateDictionary validationResults)\n'
                '{\n'
                ' if (!string.isNullOrEmpty(model.fornavn) && '
                '!string.isNullOrEmpty(model.etternavn)\n'
                ' && model.fornavn.Length + model.etternavn.Length > 50)\n'
                ' {\n'
                ' validationResults.addModelError(nameof(model.fornavn),\n'
                ' "Full name can not be longer than 50 characters.");\n'
                ' validationResults.addModelError(nameof(model.etternavn),\n'
                ' "Full name can not be longer than 50 characters.");\n'
                ' } \n'
                ' else\n'
                ' {\n'
                ' validationResults.addModelError(nameof(model.fornavn),\n'
                ' "\\*FIXED\\*Full name can not be longer than 50 '
                'characters.");\n'
                ' validationResults.addModelError(nameof(model.etternavn),\n'
                ' "\\*FIXED\\*Full name can not be longer than 50 '
                'characters.");\n'
                ' }\n'
                '}\n'
                '\n'
                '```\n'
                'If you are having trouble with getting this to work, and you '
                'are instead seeing validation messages that include the '
                '`*FIXED*`-prefix,\n'
                'double check that you have `"FixedValidationPrefix": '
                '"*FIXED*"` set under `GeneralSettings` in '
                '`appsettings.json`.\n'
                '\n'
                'Soft validations\n'
                '----------------\n'
                '\n'
                'Soft validations are validation messages that does not stop '
                'the user from submitting or move onto the next step of the '
                'process, but that are used to give the user different forms '
                'of information.\n'
                'These types of validations can for example be used to ask the '
                'user to verify input that seems wrong or strange, but which '
                'strictly speaking is not invalid, or give useful information '
                'for further filling out the form.\n'
                '\n'
                'Messages based on soft validation will be displayed once, but '
                'the user can choose to move on without making any changes.\n'
                '\n'
                'Soft validations are added from the server-side the '
                'application logic, in the same way as regular validation '
                'errors. The difference is that the validation message\n'
                'must be prefixed with the type of validation you want to '
                'give, e.g. `*WARNING*`. This will be interpreted as a soft '
                'validation. The prefix `*WARNING*` will not be displayed for '
                'the user.\n'
                '\n'
                'The different types of soft validations are `WARNING`, `INFO` '
                'and `SUCCESS`.\n'
                '\n'
                '**Code example**\n'
                '\n'
                '\n'
                '```\n'
                'public async Task ValidateData(object data, '
                'ModelStateDictionary modelState)\n'
                '{\n'
                ' if (data is TestModel testModel)\n'
                ' {\n'
                ' string firstName = testModel?.Person?.FirstName;\n'
                ' if (firstName != null && firstName.Contains("1337")) \n'
                ' {\n'
                ' validationResults.AddModelError(\n'
                ' "Person.FirstName", \n'
                ' "\\*WARNING\\*Are you sure your first name contains '
                '1337?");\n'
                ' }\n'
                '\n'
                ' if (firstName != null && firstname.Contains("Altinn"))\n'
                ' {\n'
                ' validationResults.AddModelError(\n'
                ' "Person.FirstName", \n'
                ' "\\*SUCCESS\\*Altinn is a great name!");\n'
                ' }\n'
                ' }\n'
                ' \n'
                ' await Task.CompletedTask;\n'
                '}\n'
                '\n'
                '```\n'
                'Examples on display of different validations below:\n'
                '\n'
                '[![&ldquo;Information message&rdquo;](info-message.jpeg '
                '"Example on information message (*INFO* - '
                'prefix)")](info-message.jpeg)*Example on information message '
                '(\\*INFO\\* - prefix)*[![&ldquo;Success '
                'message&rdquo;](success-message.jpeg "Example on success '
                'message (*SUCCESS* - prefix)")](success-message.jpeg)*Example '
                'on success message (\\*SUCCESS\\* - prefix)*[![&ldquo;Warning '
                'message&rdquo;](warning-message.jpeg "Example on warning '
                'message (*WARNING* - prefix)")](warning-message.jpeg)*Example '
                'on warning message (\\*WARNING\\* - prefix)*It is also '
                'possible to overrule the title you see on the messages by '
                'adding the keys `soft_validation.info_title`, '
                '`soft_validation.warning_title`, and '
                '`soft_validation.success_title` in the text resources if you '
                'want to set a custom title.\n'
                '\n'
                'Group validation\n'
                '----------------\n'
                '\n'
                'It is possible to apply validations to a repeating group when '
                'the user saves a row in the group.\n'
                'This can be done by adding a trigger on the group component '
                'in the layout file (e.g. `FormLayout.json`).\n'
                'There are two different triggers that can be used for groups; '
                '`validation` runs validation on the entire group,\n'
                'and `validateRow` only runs validation on the row the user is '
                'trying to save. Example:\n'
                '\n'
                '\n'
                '```\n'
                '{\n'
                ' "data": {\n'
                ' "layout": [\n'
                ' {\n'
                ' "id": "demo-gruppe",\n'
                ' "type": "Group",\n'
                ' "children": [\n'
                ' "..."\n'
                ' ],\n'
                ' "maxCount": 3,\n'
                ' "dataModelBindings": {\n'
                ' "group": '
                '"Endringsmelding-grp-9786.OversiktOverEndringene-grp-9788"\n'
                ' },\n'
                ' "triggers": ["validateRow"] // <--- Add this\n'
                ' },\n'
                ' ...\n'
                ' ]\n'
                ' }\n'
                '}\n'
                '\n'
                '```\n'
                'This will ensure that validation is run on the components '
                'that are a part of the group in the row you’re working on.\n'
                'If there are validation errors you will be stopped from '
                'saving the group until this has been corrected.\n'
                '\n'
                'If you add validation on the group component, a call will be '
                'made towards the validation back-end with a header specifying '
                'which component triggered the validation: `ComponentId`.\n'
                'Additionally, the row index of the row being saved is '
                'available in the header `RowIndex`. If the group is a nested '
                'group, a comma separated list of row indices is returned, '
                'otherwise it is a single number.\n'
                'Validations are written in C# in the '
                '`ValidationHandler.cs`-file in the application template. In '
                'the validation, you can retrieve component id and tailor '
                'possible validations to run in the back-end, example:\n'
                '\n'
                '\n'
                '```\n'
                'public async Task ValidateData(object data, '
                'ModelStateDictionary validationResults)\n'
                '{\n'
                ' if (data is flyttemelding model)\n'
                ' {\n'
                ' \\_httpContextAccessor.HttpContext\n'
                ' .Request.Headers\n'
                ' .TryGetValue("ComponentId", out StringValues compIdValues);\n'
                '\n'
                ' \\_httpContextAccessor.HttpContext\n'
                ' .Request.Headers\n'
                ' .TryGetValue("RowIndex", out StringValues rowIndexValues);\n'
                '\n'
                ' string componentId = '
                'compIdValues.FirstOrDefault(string.Empty);\n'
                '\n'
                ' switch (componentId)\n'
                ' {\n'
                ' case "top-level-group":\n'
                ' // run validations specific to the group\n'
                ' \n'
                ' // Get row index for a non-nested group\n'
                ' int rowIndex = '
                'int.Parse(rowIndexValues.FirstOrDefault(string.Empty));\n'
                '\n'
                ' break;\n'
                ' case "nested-group":\n'
                ' // Get all row indices for a nested group\n'
                ' int[] rowIndices = rowIndexValues\n'
                ' .FirstOrDefault(string.Empty)\n'
                ' .Split(",", StringSplitOptions.RemoveEmptyEntries)\n'
                ' .Select(s => int.Parse(s))\n'
                ' .ToArray();\n'
                '\n'
                ' break;\n'
                ' default:\n'
                ' // run the validations in their entirety\n'
                ' break;\n'
                ' }\n'
                ' }\n'
                '}\n'
                '\n'
                '```\n'
                'For tips on how you solve complex validations, see the '
                'examples under [single field '
                'validation](#single-field-validation).\n'
                '\n',
    'url': 'https://docs.altinn.studio/app/development/logic/validation/'}]
loaded markdown docs
[ Document(page_content='Group displayed as panel\n\nConfiguration details for groups displayed as panels, and referencing group values in a panel\n\nDisplay group as part of Panel\n\nOn a Group component, the parameter panel can be set up.\nThis says that the group should be displayed as part of the Panel component.\n\nHere, you will recognize the appearance and settings that can be set on the panel component. Example configuration:\n\n```\n{\n "id": "input-panel-group",\n "type": "Group",\n "children": [\n "child1",\n "child2"\n ],\n "dataModelBindings": {},\n "textResourceBindings": {\n "title": "This is just a demo of input panel outside of repeating group",\n "body": "Here I just see that things work as expected."\n },\n "panel": {\n "variant": "info"\n }\n}\n\n```\nHere the group has been set up to be displayed as a panel with the variant “info”. The setup is otherwise exactly the same as a regular group.\n\nThis will give the following output:\n\nGroup with panelIt is possible to configure the following settings in the panel field of a group:\n\n| Parameter | Required | Description |\n| --- | --- | --- |\n| variant | Yes | Which variant of panel the group should be placed in. Available values are “info”, “success” and “warning” |\n| iconUrl | No | If you want your own icon as part of a panel, this can be set. Relative or full path, e.g. “awesomeIcon.png” or “http://cdn.example.com/awesomeIcon.png" |\n| iconAlt | No | Alternate text for the custom icon. Can only be set if iconUrl has been set. Can be plain text or a reference to a text resource. |\n| groupReference | No | Reference to a different (repeating) group. Can be used if you wish to add elements to a repeating group from some other context. Read more. |\n\nExample:\n\n```\n{\n "id": "input-panel-group",\n "type": "Group",\n "panel": {\n "variant": "info",\n "iconUrl": "kort.svg",\n "iconAlt": "Betalingskort ikon"\n }\n}\n\n```\n\nAdd element from separate repeating group\n\nA use case one can imagine is that the user is asked to choose from an already filled out repeating group. One possible case is that the user is registering a set of suspicious transactions.\nHere, the user first enters a set of separate payment cards as a repeating group. Later on in the form, the user will choose elements from this group when adding a suspicious transaction.\nWhile filling out the suspicious transaction, the user remembers that they forgot to add a payment card, but do not wish to navigate all the way back to the original payment card group.\n\nThis is where the groupReference parameter comes in handy. This will open up for the possibility to add an element to a repeating group from the context from which you are using this list.\n\nA picture to illustrate the use case:\n\nGroupReference caseIn this fictitious case the groups are placed directly above each other, but imagine that these are filled out on different pages in the form.\nTo achieve this setup, a group of elements are added to the repeating group that is set up with transactions (group-2) with a reference to the first group with payment cards (group-1).\nThe following group component is one of the children of group-2:\n\n```\n{\n "id": "input-panel-group",\n "type": "Group",\n "maxCount": 3,\n "dataModelBindings": {\n "group": "Payment.Cards"\n },\n "textResourceBindings": {\n "title": "Legg til nytt betalingskort",\n "body": "Kortet du registrer vil bli lagret og tilgjengelig i resten av tjenesten.",\n "add_label": "Legg til nytt betalingskort"\n },\n "panel": {\n "showIcon": true,\n "iconUrl": "kort.svg",\n "variant": "success",\n "groupReference": {\n "group": "first-group"\n }\n }\n}\n\n```\nThe text resources that can be set are:\n\ntitle - panel title\n\nbody - panel body. Placed above the group elements.\n\nadd_label - text for the “add new”-button.\n\nIf children is not set on the group, the children of the referenced group will be rendered.\nBy adding to children you can freely define that only a subset of all children of the referenced group should be displayed.\n\nDemonstration:\n\nDemonstration of groupReferenceSee example app for complete setup in form layout.', metadata={'source': '/var/folders/01/_86bbblx2hj_1_w6b8wpn9jm0000gn/T/tmpp0dwjyjk/__docs.altinn.studio_app_development_ux_fields_grouping_panel_.md'}),
  Document(page_content='Multiple pages within a group\n\nHow to show components in a group in multiple pages\n\nMultiple pages within group-display\n\nThis functionality is as of today only available for repeating groups. Displaying of groups over\nmultiple pages inside the editing area of the group is only supported for groups at the top level, and is not supported\nfor nested groups.When entering data in a group, there may be incidents where each element in the group contains multiple fields, which may result in a lot of scrolling\nand confusion for the user. To solve this, there has been implemented a possibility to split the fill out over multiple pages, which the user can navigate\nthrough while filling out the group element. The navigation takes place within a layout, and updates\nonly the display within the editing area of the group.\n\n```\n{\n "id": "Some-group-id",\n "type": "Group",\n "children": [\n "0:fnr",\n "1:fornavn",\n "1:mellomnavn",\n "1:etternavn"\n ],\n "maxCount": 10,\n "dataModelBindings": {\n "group": "familie.barn"\n },\n "edit": {\n "multiPage": true,\n "mode": "hideTable",\n }\n}\n\n```\nHere a mode that hides the table when editing has also been added.\nThe result will be as displayed below.\n\nFill-out of group over multiple pages', metadata={'source': '/var/folders/01/_86bbblx2hj_1_w6b8wpn9jm0000gn/T/tmpp0dwjyjk/__docs.altinn.studio_app_development_ux_fields_grouping_repeating_multipage_.md'}),
  Document(page_content='Repeating groups\n\nSetup for repeating groups\n\nGroups in the data model contain one or more fields. Groups are defined as repeating if they have maxCount > 1 in\nthe layout configuration. A group that is repeating in the data model must also be set up as repeating in the form, if\nnot, data saving will fail. In JSON, a repeating group is defined as an array of objects, where each object is a group.\nIn XML, a repeating group is defined as a list of elements, where each element is a group/object with properties.\n\nExample\n\nBelow is a form with a repeating group that:\n\nContains two components (checkbox and address)\n\nCan be repeated up to three times\n\nIs bound to the data model group/array GruppeListe\n\nForm with repeating groupVis/skjul innhold\nShow configuration for this screenshot\n```\n 1[\n 2 {\n 3 "id": "gruppe",\n 4 "type": "Group",\n 5 "children": [\n 6 "avkrysningsboks",\n 7 "adresse"\n 8 ],\n 9 "maxCount": 3,\n10 "dataModelBindings": {\n11 "group": "GruppeListe"\n12 }\n13 },\n14 {\n15 "id": "avkrysningsboks",\n16 "type": "Checkboxes",\n17 "textResourceBindings": {\n18 "title": "Avkrysningsboks"\n19 },\n20 "dataModelBindings": {\n21 "simpleBinding": "GruppeListe.Avkrysning"\n22 },\n23 "options": [\n24 {\n25 "label": "Navn",\n26 "value": "Verdi1"\n27 },\n28 {\n29 "label": "Adresse",\n30 "value": "Verdi2"\n31 }\n32 ],\n33 "required": true\n34 },\n35 {\n36 "id": "addresse",\n37 "type": "AddressComponent",\n38 "textResourceBindings": {\n39 "title": "Adresse" \n40 },\n41 "dataModelBindings": {\n42 "address": "GruppeListe.Adresse",\n43 "zipCode": "GruppeListe.Postnr",\n44 "postPlace": "GruppeListe.Poststed"\n45 },\n46 "simplified": true,\n47 "readOnly": false,\n48 "required": true\n49 }\n50]\n\n```\nParameters\n\n| Parameter | Required | Description |\n| --- | --- | --- |\n| id | Yes | Unique ID, same as ID on other components. Must be unique in the layout file, and should be unique across pages. |\n| type | Yes | Must be ‘Group’ |\n| dataModelBindings | No | Must be set for repeating groups with form components inside. Should point to the repeating group in the data model. |\n| textResourceBindings | No | Can be set for repeating groups, see description. |\n| maxCount | Yes | The number of times a group can repeat. Must be set to 1 or more for the group component to work as a repeating group. |\n| minCount | No | Validation. The minimum number of times a group must repeat before the user can submit the form. |\n| children | Yes | List of the component IDs that are to be included in the repeating group. |\n|  | No | Options for how to display the group when editing a row. |\n| tableHeaders | No | List of components that are to be included as part of the table header fields. If not specified, all components are displayed. |\n| tableColumns | No | Object containing column options for specified headers. If not specified, all columns will use default display settings. |\n\ntextResourceBindings\n\nIt is possible to add different keys in textResourceBindings to overrule default texts.\n\ntitle - title to show above the group row in a Summary component.\n\nadd_button - is added at the end of the “Add new” text on the button, and can be used to e.g. get text that says “Add new person”.\n\nadd_button_full - is used as custom text on the “Add new” button. Overrides add_button if both are set.\n\nsave_button - is used as text on the “Save” button when the user is filling out data.\n\nsave_and_next_button - is used as text on the “Save and open next” button if enabled.\n\nedit_button_open - is used as text on the “Edit” button on the table when the user is opening an element.\n\nedit_button_close - is used as text on the “Edit” button on the table when the user is closing an element.\n\nRow editing settingsChange how to edit/fill out a row in a repeating group\n\nTable configurationConfiguration for the table that is shown above repeating groups\n\nAttachments in repeating groupsSpecifics on how to set up attachment uploading in repeating groups\n\nDynamic behaviour in repeating groupsHow to hide rows in a repeating group\n\nMultiple pages within a groupHow to show components in a group in multiple pages', metadata={'source': '/var/folders/01/_86bbblx2hj_1_w6b8wpn9jm0000gn/T/tmpp0dwjyjk/__docs.altinn.studio_app_development_ux_fields_grouping_repeating_.md'}),
  Document(page_content='Validation\n\nHow to add logic to validate form data?\n\nOn this page:\n\nIntroduction\n\nClient-side validation\n\nServer-side validation\n\nHow to add custom validation\n\nSingle field validation\n\nSoft validations\n\nGroup validation\nIntroduction\n\nValidations ensures that the user’s input is valid with regard to the data model,\nin addition to all custom rules that are set up for the application.\nValidations can be run either on the client- (the browser) or the server-side.\n\nValidations can also be set up to trigger on page navigation.\n\nClient-side validation\n\nThis is validation that is run in the browser, before data is sent to server for saving. This makes it possible to give quick feedback to\nthe user during the process of filling out the form.\n\nClient-side validation is based on the data model of the form, and uses this to determine what is valid input in a\nfield.\nSpecifically, the JSON schema version of the data model is used for validation. This is automatically generated when\nuploading an XSD.\nIt is possible to make changes in the JSON schema file directly to adapt the validation when needed.\n\nNote that if you make changes in the JSON schema manually, and then update the XSD and re-upload it, a new\nJSON schema will also be generated and all manual adaptations will have to be remade. It is therefore recommended to\nmake changes in the XSD and/or the data modeling tool\nfor these changes to be reflected in the JSON schema.\n\nAn example of how a field can be defined in the JSON schema data model is:\n\n```\n"someField": {\n "type": "string",\n "maxLength": "4"\n}\n\n```\nInput in this field will be validated towards the limits that are set, and an error message will appear if these are not met - in this case, if\ninput is a text longer than four characters.\n\nDefault error messages\n\nDefault error messages has been set up for all validations done on the client-side. See the overview below.\n\n| Rule | Error message bokmål | Error message nynorsk | Error message english |\n| --- | --- | --- | --- |\n| min | ‘Minste gyldig verdi er {0}’ | ‘Minste gyldig verdi er {0}’ | ‘Minimum valid value is {0}’ |\n| max | ‘Største gyldig verdi er {0}’ | ‘Største gyldig verdi er {0}’ | ‘Maximum valid value is {0}’ |\n| minLength | ‘Bruk {0} eller flere tegn’ | ‘Bruk {0} eller flere tegn’ | ‘Use {0} or more characters’ |\n| maxLength | ‘Bruk {0} eller færre tegn’ | ‘Bruk {0} eller færre tegn’ | ‘Use {0} or fewer characters’ |\n| length | ‘Antall tillatte tegn er {0}’ | ‘Antall tillatte tegn er {0}’ | ‘Number of characters allowed is {0}’ |\n| pattern | ‘Feil format eller verdi’ | ‘Feil format eller verdi’ | ‘Wrong format or value’ |\n| required | ‘Du må fylle ut {0}’ | ‘Du må fylle ut {0}’ | ‘You have to fill out {0}’ |\n| enum | ‘Kun verdiene {0} er tillatt’ | ‘Kun verdiene {0} er tillatt’ | ‘Only the values {0} are permitted’ |\n\nMore about error messages for required fields\n\nFor a smoother user experience, error messages for missing data in required fields won’t be displayed automatically\nwhile filling out a form, unless validation is triggered for a single field, when saving\na row in a repeating group or\nwhen navigating to another page.\n\nThe error message for required fields is as defined above, “You have to fill out {0}”. The {0} symbol is replaced with the field that\nthe error message is shown for. This is done in the following way:\n\nIf shortName text is defined for the component, this is used. This is a new text that is currently used only for this specific error message.\n\nIf the shortName text is not defined, the title text for the component is used - this is the components label text. The text will be converted to use a lowercase letter first, unless the text looks like an acronym.\n\nIn some special cases (Address component) where there are multiple fields within the component, the default labels for the fields is used.\n\nExample: Component with only title\n\n```\n{\n "id": "firstName",\n "type": "Input",\n "textResourceBindings": {\n "title": "text-firstName"\n },\n ... //etc\n}\n\n```\nWith resource texts:\n\n```\n...\n{\n "id": "text-firstName",\n "value": "First name"\n}\n\n``\nThe error message would then be"You have to fill out First name"`.\n\nExample: Component with shortName\n\nIf the field’s prompt is long or not suitable for use in the validation message, you can add a shortName text that can be used instead.\nNote that this only applies to this specific validation message - the shortName text is not used otherwise in the solution as of now.\n\n```\n{\n "id": "firstName",\n "type": "Input",\n "textResourceBindings": {\n "title": "text-firstName",\n "shortName": "firstName-short",\n },\n ... //etc\n}\n\n```\nWith resource texts:\n\n```\n...\n{\n "id": "text-firstName",\n "value": "Please type your first name in the field below:"\n},\n{\n "id": "firstName-short",\n "value": "your first name"\n}\n\n``\nThe error message would then be"You have to fill out your first name"`.\n\nCustom error messages\n\nIt is possible to define custom error messages that will be displayed when a field doesn’t pass the validation check. This is done by including a parameter errorMessage where the field is defined in the JSON schema.\nThe JSON schema file is in the folder App/models and has a naming patterns as follows; *.schema.json,\n\nAn example of how to extend the example previously presented with a custom error message:\n\n```\n"someField": {\n "type": "string",\n "maxLength": "4",\n "errorMessage": "myCustomError"\n}\n\n```\nThe error text can be included directly. To enable language support, add a text key for a text defined in the resource files.\n\nNotice that if you have a reference to a definition the error message must be added to the property-field and not the reference/definition.\nExample:\n\n```\n{\n "properties": {\n "person": {\n "$ref" : "#/definitions/personDefinition",\n "errorMessage": "myCustomError",\n }\n },\n "definitions": {\n "personDefinition" : {\n "age": {\n "type": "number"\n },\n ...\n }\n}\n\n```\nNote that when the XSD is changed, the custom error messages will de removed from the JSON schema.\nIn the future, there will be support for setting custom error messages in the data modelling tool in Altinn Studio. But for now, this is a manual job.Server-side validation\n\nServer-side validation can be split into two categories:\n\nValidations against data model - These run automatically whenever the user attempts to submit form data.\n\nCustom validations - these are written by the application developer,\nand run when the user attempts to submit form data or move the process to a new step.\n\nHow to add custom validation\n\nCustom validation can also be split into two categories; task-validation and data-validation.\n\nTask-validation will run each time validation is triggered either manually from the application or when you attempt to move forward in the process.\n\nData-validation will run if you’re on a step that has defined data elements associated with it.\n\nValidations are written i C# and depending on the version of the application template and Nuget packages you are using,\nthe way the implementation is done varies slightly. In the earlier versions it’s a pre-created file where you put your\nlogic, while from version 7 and onwards you implement an interface in whatever class you like. The interface happens to\nbe equal to the pre-defined class in the earlier versions. The examples below which referrers to the methods to add your\nvalidation logic to is the same.\n\nv7In version 7 the way to do custom code instantiation has changed. We now use an dependency injection based approach\ninstead of overriding methods. If you previously used to place your custom code in the ValidateData and ValidateTask\nmethods in the ValidationHandler.cs class you will see that it’s mostly the same.\n\nCreate a class that implements the IInstanceValidator interface found in the Altinn.App.Core.Features.Validation namespace.\nYou can name and place the file in any folder you like within your project, but we suggest you use meaningful namespaces like in any other .Net project.\n\nRegister you custom implementation in the Program.cs class\n```\nservices.AddTransient();\n\n``\nThis ensures your custom code is known to the application and that it will be executed.\nv4, v5, v6\nValidations should be added to theValidationHandler.cs-file in the application template.\nThe file can be accessed and edited in Altinn Studio through the logic menu, by selecting *Rediger valideringer*,\nor directly in the application repo where the file is under thelogic/Validation`-folder.From here on the examples should be valid for all versions:)\n\nCustom logic are added to the ValidateData and ValidateTask-methods.\nThe former takes in a data object and the latter takes in the instance and taskId.\nTo add a validation error, the AddModelError-method of the validationResult-object, which is a parameter in both methods, is used.\n\nAn example of a simple data validation that tests that the field FirstName does not contain the value 1337, when the root element of the model is Skjema is shown below:\n\n```\npublic void ValidateData(object data, ModelStateDictionary validationResults)\n{\n if (data.GetType() == typeof(Skjema))\n {\n // Cast instance data to model type\n Skjema model = (Skjema)data;\n\n// Get value to test - FirstName\n string firstName = Skjema?.Person?.FirstName;\n\n// Check if FirstName exists, and contains the value "1337"\n if (firstName != null && firstName.Contains("1337"))\n {\n // Add validation error, with error message and list\n // of affected fields (in this case Person.FirstName)\n validationResults.AddModelError(\n "Person.FirstName",\n "Error: First name cannot contain the value \'1337\'."\n );\n }\n }\n}\n\n```\nSee comments in code above for an explanation of what the different parts do.\n\nIn the other parameter of the method AddModelError, where it says “Error: First name cannot contain the value \'\n1337’”, you can use a text key for a text defined in the resource files for multilingual support.\n\nAn example of a simple task validation that checks how long the user spent on Task_1 and returns an error if there has gone more than three days:\n\n```\npublic async Task ValidateTask(Instance instance, string taskId, ModelStateDictionary validationResults)\n{\n if (taskId.Equals("Task_1"))\n {\n DateTime deadline = ((DateTime)instance.Created).AddDays(3);\n if (DateTime.UtcNow < deadline)\n {\n validationResults.AddModelError("Task_1", $"Completion of Task_1 has taken too long. Please start over.");\n }\n }\n}\n\n```\nSingle field validation\n\nIf there is a need for immediate validation of a field\nthat can not be covered in the client side validation,\nyou can set up a trigger for validation on single fields in formLayout.json\n\nNOTE: Trigger for validation on single fields in Stateless apps is not currently supported.\n```\n{\n "data": {\n "layout": [\n {\n "id": "3611fb2a-c06b-4fa7-a400-3f6c1ece64e1",\n "textResourceBindings": {\n "title": "25795.OppgavegiverNavnPreutfyltdatadef25795.Label"\n },\n "dataModelBindings": {\n "simpleBinding": "etatid"\n },\n "type": "Input",\n "triggers": ["validation"] , // <--- Add this field\n },\n {\n "id": "9ec368da-d6a9-4fbd-94d0-b4dfa8891981",\n "type": "Button",\n "textResourceBindings": {\n "title": "Button"\n },\n "dataModelBindings": {},\n "textResourceId": "Standard.Button.Button",\n "customType": "Standard"\n }\n ]\n }\n}\n\n``\nNote that if you define a field to trigger validation server-side, only the result of this validation will be displayed. Meaning,\nif there is another client-side validation defined, a possible server-side validation of the field will overwrite these. Therefore, you should make sure\nto implement all necessary validations on the server-side as well. It is possible to attach multiple error messages to the same field if needed.The configuration above will result in your own custom validation inValidationHandler.cs`\nbeing triggered each time the field is updated. If you need to know which field\ntriggered the validation, this is available in the http-context as a header of the request named ValidationTriggerField.\n\nAn example of a custom validation where the header value is retrieved is shown below.\n\n```\n public async Task ValidateData(object data, ModelStateDictionary validationResults)\n {\n _httpContextAccessor.HttpContext\n .Request.Headers\n .TryGetValue("ValidationTriggerField", out StringValues triggerValues);\n\nstring triggerField = triggerValues.FirstOrDefault(string.Empty);\n\nif (triggerField.Equals("kommune"))\n {\n // Cast instance data to model type\n flyttemelding model = (flyttemelding)data;\n\n// Get value to test - Kommune\n string kommune = model.kommune;\n\nif (!kommune.Equals("Oslo"))\n {\n validationResults.AddModelError(triggerField, "This is not a valid municipality.");\n }\n }\n\nawait Task.CompletedTask;\n }\n\n```\nNOTE validation of single fields should be implemented in a way where it is both run on triggers and during general validation.\nThe example that revolves multiple complex validations show how this can be implemented.\n\nSeveral things has been done to get this code to run\n\nIn ValidationHandler.cs using Microsoft.Extensions.Primitives; is included at the top of the file to be able to use StringValues.\n\nIn App.cs using Microsoft.AspNetCore.Http; is included at the top of the file to be able to use IHttpContextAccessor.\n\nIn App.cs IHttpContextAccessor is dependency injected in the constructor and passed along to ValidationHandler.\n\n```\npublic App(\n IAppResources appResourcesService,\n ILogger logger,\n IData dataService,\n IProcess processService,\n IPDF pdfService,\n IProfile profileService,\n IRegister registerService,\n IPrefill prefillService,\n IHttpContextAccessor httpContextAccessor // <--- Add this line\n ) : base(appResourcesService, logger, dataService, processService, pdfService, prefillService)\n {\n _logger = logger;\n _validationHandler = new ValidationHandler(httpContextAccessor); // <--- Include the new property here\n _calculationHandler = new CalculationHandler();\n _instantiationHandler = new InstantiationHandler(profileService, registerService);\n }\n\n```\nIf there are multiple complex validations that are time consuming, it is recommended to implement several private methods\nto validate these and use ValidationTriggerField to determine which private method is to be run.\nYou can e.g. use a switch statement to accomplish this.\n\n```\npublic async Task ValidateData(object data, ModelStateDictionary validationResults)\n{\n if (data is flyttemelding model)\n {\n _httpContextAccessor.HttpContext\n .Request.Headers\n .TryGetValue("ValidationTriggerField", out StringValues triggerValues);\n\nstring triggerField = triggerValues.FirstOrDefault(string.Empty);\n\nswitch (triggerField)\n {\n case "kommune":\n ValidateKommune(model, validationResults);\n break;\n case "boaddresse":\n ValidateBoAdresse(model, validationResults);\n break;\n default:\n ValidateKommune(model, validationResults);\n ValidateBoAdresse(model, validationResults);\n break;\n }\n }\n}\n\nprivate void ValidateKommune(flyttemelding model, ModelStateDictionary validationResults)\n{\n if (model.kommune != null && !model.kommune.Equals("Oslo"))\n {\n validationResults.AddModelError(\n nameof(model.kommune), \n "This is not a valid municipality.");\n }\n}\nprivate void ValidateBoAdresse(flyttemelding model, ModelStateDictionary validationResults)\n{\n if (model.boaddresse != null && model.boaddresse.Length > 150)\n {\n validationResults.AddModelError(\n nameof(model.boaddresse), \n "Address can not be longer than 150 characters.");\n }\n}\n\n```\n\nSpecify that validation errors are fixed\n\nWhen validation is triggered by a single field, all former validations on this field will be removed pending a response from the last validation.\nIf a field triggers validation that updates/adds an error message to multiple fields at once, these will not be removed even when there no longer are any\nerrors in these fields. This is because there is no way to know which fields may have been validated through a single field validation.\n\nFor example, if you have two fields; first name and last name. Both fields trigger single field validation, and if both fields have a value, you can validate that\nthe full name can not be longer than 50 characters. An error message is then set on both fields. If you correct this by changing the first name, the error message from first name will\ndisappear, but the error message on the last name field will still be displayed even though the validation does not set any error messages on the fields.\n\n```\nprivate void ValidateFullName(Datamodell model, ModelStateDictionary validationResults)\n{\n if (!string.isNullOrEmpty(model.fornavn) && !string.isNullOrEmpty(model.etternavn)\n && model.fornavn.Length + model.etternavn.Length > 50)\n {\n validationResults.addModelError(nameof(model.fornavn),\n "Full name can not be longer than 50 characters.");\n validationResults.addModelError(nameof(model.etternavn),\n "Full name can not be longer than 50 characters.");\n }\n}\n\n```\nTo be able to remove old error messages in a case like this, there has been added support to be able to specify that a validation error has been fixed.\nThen, the field in question will be able to be notified that a specific error message that it is displaying has been fixed and can now be hidden.\n\nThis is done by adding a validation error in the code in the case where there are no errors in the validation,\nand set *FIXED* in front of the error message itself. This corresponds to the setup for soft validation.\nThis prefix causes the error message that is set to be removed from the field in question, or ignored (if there is no error message on the field already).\n\nYou can now expand the example above to support this:\n\n```\nprivate void ValidateFullName(Datamodell model, ModelStateDictionary validationResults)\n{\n if (!string.isNullOrEmpty(model.fornavn) && !string.isNullOrEmpty(model.etternavn)\n && model.fornavn.Length + model.etternavn.Length > 50)\n {\n validationResults.addModelError(nameof(model.fornavn),\n "Full name can not be longer than 50 characters.");\n validationResults.addModelError(nameof(model.etternavn),\n "Full name can not be longer than 50 characters.");\n } \n else\n {\n validationResults.addModelError(nameof(model.fornavn),\n "*FIXED*Full name can not be longer than 50 characters.");\n validationResults.addModelError(nameof(model.etternavn),\n "*FIXED*Full name can not be longer than 50 characters.");\n }\n}\n\nSoft validations\n\nSoft validations are validation messages that does not stop the user from submitting or move onto the next step of the process, but that are used to give the user different forms of information.\nThese types of validations can for example be used to ask the user to verify input that seems wrong or strange, but which strictly speaking is not invalid, or give useful information for further filling out the form.\n\nMessages based on soft validation will be displayed once, but the user can choose to move on without making any changes.\n\nSoft validations are added from the server-side the application logic, in the same way as regular validation errors. The difference is that the validation message\nmust be prefixed with the type of validation you want to give, e.g. *WARNING*. This will be interpreted as a soft validation. The prefix *WARNING* will not be displayed for the user.\n\nThe different types of soft validations are WARNING, INFO and SUCCESS.\n\nCode example\n\n```\npublic async Task ValidateData(object data, ModelStateDictionary modelState)\n{\n if (data is TestModel testModel)\n {\n string firstName = testModel?.Person?.FirstName;\n if (firstName != null && firstName.Contains("1337")) \n {\n validationResults.AddModelError(\n "Person.FirstName", \n "*WARNING*Are you sure your first name contains 1337?");\n }\n\nif (firstName != null && firstname.Contains("Altinn"))\n {\n validationResults.AddModelError(\n "Person.FirstName", \n "*SUCCESS*Altinn is a great name!");\n }\n }\n\nawait Task.CompletedTask;\n}\n\n```\nExamples on display of different validations below:\n\nGroup validation\n\nIt is possible to apply validations to a repeating group when the user saves a row in the group.\nThis can be done by adding a trigger on the group component in the layout file (e.g. FormLayout.json).\nThere are two different triggers that can be used for groups; validation runs validation on the entire group,\nand validateRow only runs validation on the row the user is trying to save. Example:\n\n```\n{\n "data": {\n "layout": [\n {\n "id": "demo-gruppe",\n "type": "Group",\n "children": [\n "..."\n ],\n "maxCount": 3,\n "dataModelBindings": {\n "group": "Endringsmelding-grp-9786.OversiktOverEndringene-grp-9788"\n },\n "triggers": ["validateRow"] // <--- Add this\n },\n ...\n ]\n }\n}\n\n```\nThis will ensure that validation is run on the components that are a part of the group in the row you’re working on.\nIf there are validation errors you will be stopped from saving the group until this has been corrected.\n\nIf you add validation on the group component, a call will be made towards the validation back-end with a header specifying which component triggered the validation: ComponentId.\nAdditionally, the row index of the row being saved is available in the header RowIndex. If the group is a nested group, a comma separated list of row indices is returned, otherwise it is a single number.\nValidations are written in C# in the ValidationHandler.cs-file in the application template. In the validation, you can retrieve component id and tailor possible validations to run in the back-end, example:\n\n```\npublic async Task ValidateData(object data, ModelStateDictionary validationResults)\n{\n if (data is flyttemelding model)\n {\n _httpContextAccessor.HttpContext\n .Request.Headers\n .TryGetValue("ComponentId", out StringValues compIdValues);\n\n_httpContextAccessor.HttpContext\n .Request.Headers\n .TryGetValue("RowIndex", out StringValues rowIndexValues);\n\nstring componentId = compIdValues.FirstOrDefault(string.Empty);\n\nswitch (componentId)\n {\n case "top-level-group":\n // run validations specific to the group\n\n// Get row index for a non-nested group\n int rowIndex = int.Parse(rowIndexValues.FirstOrDefault(string.Empty));\n\nbreak;\n case "nested-group":\n // Get all row indices for a nested group\n int[] rowIndices = rowIndexValues\n .FirstOrDefault(string.Empty)\n .Split(",", StringSplitOptions.RemoveEmptyEntries)\n .Select(s => int.Parse(s))\n .ToArray();\n\nbreak;\n default:\n // run the validations in their entirety\n break;\n }\n }\n}\n\n```\nFor tips on how you solve complex validations, see the examples under single field validation.', metadata={'source': '/var/folders/01/_86bbblx2hj_1_w6b8wpn9jm0000gn/T/tmpp0dwjyjk/__docs.altinn.studio_app_development_logic_validation_.md'})]


[1m> Entering new StuffDocumentsChain chain...[0m


[1m> Entering new LLMChain chain...[0m
Prompt after formatting:
[32;1m[1;3mSystem: Use the following pieces of context to answer the users question. 
If you don't know the answer, just say that you don't know, don't try to make up an answer.
----------------
Group displayed as panel

Configuration details for groups displayed as panels, and referencing group values in a panel

Display group as part of Panel

On a Group component, the parameter panel can be set up.
This says that the group should be displayed as part of the Panel component.

Here, you will recognize the appearance and settings that can be set on the panel component. Example configuration:

```
{
 "id": "input-panel-group",
 "type": "Group",
 "children": [
 "child1",
 "child2"
 ],
 "dataModelBindings": {},
 "textResourceBindings": {
 "title": "This is just a demo of input panel outside of repeating group",
 "body": "Here I just see that things work as expected."
 },
 "panel": {
 "variant": "info"
 }
}

```
Here the group has been set up to be displayed as a panel with the variant “info”. The setup is otherwise exactly the same as a regular group.

This will give the following output:

Group with panelIt is possible to configure the following settings in the panel field of a group:

| Parameter | Required | Description |
| --- | --- | --- |
| variant | Yes | Which variant of panel the group should be placed in. Available values are “info”, “success” and “warning” |
| iconUrl | No | If you want your own icon as part of a panel, this can be set. Relative or full path, e.g. “awesomeIcon.png” or “http://cdn.example.com/awesomeIcon.png" |
| iconAlt | No | Alternate text for the custom icon. Can only be set if iconUrl has been set. Can be plain text or a reference to a text resource. |
| groupReference | No | Reference to a different (repeating) group. Can be used if you wish to add elements to a repeating group from some other context. Read more. |

Example:

```
{
 "id": "input-panel-group",
 "type": "Group",
 "panel": {
 "variant": "info",
 "iconUrl": "kort.svg",
 "iconAlt": "Betalingskort ikon"
 }
}

```

Add element from separate repeating group

A use case one can imagine is that the user is asked to choose from an already filled out repeating group. One possible case is that the user is registering a set of suspicious transactions.
Here, the user first enters a set of separate payment cards as a repeating group. Later on in the form, the user will choose elements from this group when adding a suspicious transaction.
While filling out the suspicious transaction, the user remembers that they forgot to add a payment card, but do not wish to navigate all the way back to the original payment card group.

This is where the groupReference parameter comes in handy. This will open up for the possibility to add an element to a repeating group from the context from which you are using this list.

A picture to illustrate the use case:

GroupReference caseIn this fictitious case the groups are placed directly above each other, but imagine that these are filled out on different pages in the form.
To achieve this setup, a group of elements are added to the repeating group that is set up with transactions (group-2) with a reference to the first group with payment cards (group-1).
The following group component is one of the children of group-2:

```
{
 "id": "input-panel-group",
 "type": "Group",
 "maxCount": 3,
 "dataModelBindings": {
 "group": "Payment.Cards"
 },
 "textResourceBindings": {
 "title": "Legg til nytt betalingskort",
 "body": "Kortet du registrer vil bli lagret og tilgjengelig i resten av tjenesten.",
 "add_label": "Legg til nytt betalingskort"
 },
 "panel": {
 "showIcon": true,
 "iconUrl": "kort.svg",
 "variant": "success",
 "groupReference": {
 "group": "first-group"
 }
 }
}

```
The text resources that can be set are:

title - panel title

body - panel body. Placed above the group elements.

add_label - text for the “add new”-button.

If children is not set on the group, the children of the referenced group will be rendered.
By adding to children you can freely define that only a subset of all children of the referenced group should be displayed.

Demonstration:

Demonstration of groupReferenceSee example app for complete setup in form layout.

Multiple pages within a group

How to show components in a group in multiple pages

Multiple pages within group-display

This functionality is as of today only available for repeating groups. Displaying of groups over
multiple pages inside the editing area of the group is only supported for groups at the top level, and is not supported
for nested groups.When entering data in a group, there may be incidents where each element in the group contains multiple fields, which may result in a lot of scrolling
and confusion for the user. To solve this, there has been implemented a possibility to split the fill out over multiple pages, which the user can navigate
through while filling out the group element. The navigation takes place within a layout, and updates
only the display within the editing area of the group.

```
{
 "id": "Some-group-id",
 "type": "Group",
 "children": [
 "0:fnr",
 "1:fornavn",
 "1:mellomnavn",
 "1:etternavn"
 ],
 "maxCount": 10,
 "dataModelBindings": {
 "group": "familie.barn"
 },
 "edit": {
 "multiPage": true,
 "mode": "hideTable",
 }
}

```
Here a mode that hides the table when editing has also been added.
The result will be as displayed below.

Fill-out of group over multiple pages

Repeating groups

Setup for repeating groups

Groups in the data model contain one or more fields. Groups are defined as repeating if they have maxCount > 1 in
the layout configuration. A group that is repeating in the data model must also be set up as repeating in the form, if
not, data saving will fail. In JSON, a repeating group is defined as an array of objects, where each object is a group.
In XML, a repeating group is defined as a list of elements, where each element is a group/object with properties.

Example

Below is a form with a repeating group that:

Contains two components (checkbox and address)

Can be repeated up to three times

Is bound to the data model group/array GruppeListe

Form with repeating groupVis/skjul innhold
Show configuration for this screenshot
```
 1[
 2 {
 3 "id": "gruppe",
 4 "type": "Group",
 5 "children": [
 6 "avkrysningsboks",
 7 "adresse"
 8 ],
 9 "maxCount": 3,
10 "dataModelBindings": {
11 "group": "GruppeListe"
12 }
13 },
14 {
15 "id": "avkrysningsboks",
16 "type": "Checkboxes",
17 "textResourceBindings": {
18 "title": "Avkrysningsboks"
19 },
20 "dataModelBindings": {
21 "simpleBinding": "GruppeListe.Avkrysning"
22 },
23 "options": [
24 {
25 "label": "Navn",
26 "value": "Verdi1"
27 },
28 {
29 "label": "Adresse",
30 "value": "Verdi2"
31 }
32 ],
33 "required": true
34 },
35 {
36 "id": "addresse",
37 "type": "AddressComponent",
38 "textResourceBindings": {
39 "title": "Adresse" 
40 },
41 "dataModelBindings": {
42 "address": "GruppeListe.Adresse",
43 "zipCode": "GruppeListe.Postnr",
44 "postPlace": "GruppeListe.Poststed"
45 },
46 "simplified": true,
47 "readOnly": false,
48 "required": true
49 }
50]

```
Parameters

| Parameter | Required | Description |
| --- | --- | --- |
| id | Yes | Unique ID, same as ID on other components. Must be unique in the layout file, and should be unique across pages. |
| type | Yes | Must be ‘Group’ |
| dataModelBindings | No | Must be set for repeating groups with form components inside. Should point to the repeating group in the data model. |
| textResourceBindings | No | Can be set for repeating groups, see description. |
| maxCount | Yes | The number of times a group can repeat. Must be set to 1 or more for the group component to work as a repeating group. |
| minCount | No | Validation. The minimum number of times a group must repeat before the user can submit the form. |
| children | Yes | List of the component IDs that are to be included in the repeating group. |
|  | No | Options for how to display the group when editing a row. |
| tableHeaders | No | List of components that are to be included as part of the table header fields. If not specified, all components are displayed. |
| tableColumns | No | Object containing column options for specified headers. If not specified, all columns will use default display settings. |

textResourceBindings

It is possible to add different keys in textResourceBindings to overrule default texts.

title - title to show above the group row in a Summary component.

add_button - is added at the end of the “Add new” text on the button, and can be used to e.g. get text that says “Add new person”.

add_button_full - is used as custom text on the “Add new” button. Overrides add_button if both are set.

save_button - is used as text on the “Save” button when the user is filling out data.

save_and_next_button - is used as text on the “Save and open next” button if enabled.

edit_button_open - is used as text on the “Edit” button on the table when the user is opening an element.

edit_button_close - is used as text on the “Edit” button on the table when the user is closing an element.

Row editing settingsChange how to edit/fill out a row in a repeating group

Table configurationConfiguration for the table that is shown above repeating groups

Attachments in repeating groupsSpecifics on how to set up attachment uploading in repeating groups

Dynamic behaviour in repeating groupsHow to hide rows in a repeating group

Multiple pages within a groupHow to show components in a group in multiple pages

Validation

How to add logic to validate form data?

On this page:

Introduction

Client-side validation

Server-side validation

How to add custom validation

Single field validation

Soft validations

Group validation
Introduction

Validations ensures that the user’s input is valid with regard to the data model,
in addition to all custom rules that are set up for the application.
Validations can be run either on the client- (the browser) or the server-side.

Validations can also be set up to trigger on page navigation.

Client-side validation

This is validation that is run in the browser, before data is sent to server for saving. This makes it possible to give quick feedback to
the user during the process of filling out the form.

Client-side validation is based on the data model of the form, and uses this to determine what is valid input in a
field.
Specifically, the JSON schema version of the data model is used for validation. This is automatically generated when
uploading an XSD.
It is possible to make changes in the JSON schema file directly to adapt the validation when needed.

Note that if you make changes in the JSON schema manually, and then update the XSD and re-upload it, a new
JSON schema will also be generated and all manual adaptations will have to be remade. It is therefore recommended to
make changes in the XSD and/or the data modeling tool
for these changes to be reflected in the JSON schema.

An example of how a field can be defined in the JSON schema data model is:

```
"someField": {
 "type": "string",
 "maxLength": "4"
}

```
Input in this field will be validated towards the limits that are set, and an error message will appear if these are not met - in this case, if
input is a text longer than four characters.

Default error messages

Default error messages has been set up for all validations done on the client-side. See the overview below.

| Rule | Error message bokmål | Error message nynorsk | Error message english |
| --- | --- | --- | --- |
| min | ‘Minste gyldig verdi er {0}’ | ‘Minste gyldig verdi er {0}’ | ‘Minimum valid value is {0}’ |
| max | ‘Største gyldig verdi er {0}’ | ‘Største gyldig verdi er {0}’ | ‘Maximum valid value is {0}’ |
| minLength | ‘Bruk {0} eller flere tegn’ | ‘Bruk {0} eller flere tegn’ | ‘Use {0} or more characters’ |
| maxLength | ‘Bruk {0} eller færre tegn’ | ‘Bruk {0} eller færre tegn’ | ‘Use {0} or fewer characters’ |
| length | ‘Antall tillatte tegn er {0}’ | ‘Antall tillatte tegn er {0}’ | ‘Number of characters allowed is {0}’ |
| pattern | ‘Feil format eller verdi’ | ‘Feil format eller verdi’ | ‘Wrong format or value’ |
| required | ‘Du må fylle ut {0}’ | ‘Du må fylle ut {0}’ | ‘You have to fill out {0}’ |
| enum | ‘Kun verdiene {0} er tillatt’ | ‘Kun verdiene {0} er tillatt’ | ‘Only the values {0} are permitted’ |

More about error messages for required fields

For a smoother user experience, error messages for missing data in required fields won’t be displayed automatically
while filling out a form, unless validation is triggered for a single field, when saving
a row in a repeating group or
when navigating to another page.

The error message for required fields is as defined above, “You have to fill out {0}”. The {0} symbol is replaced with the field that
the error message is shown for. This is done in the following way:

If shortName text is defined for the component, this is used. This is a new text that is currently used only for this specific error message.

If the shortName text is not defined, the title text for the component is used - this is the components label text. The text will be converted to use a lowercase letter first, unless the text looks like an acronym.

In some special cases (Address component) where there are multiple fields within the component, the default labels for the fields is used.

Example: Component with only title

```
{
 "id": "firstName",
 "type": "Input",
 "textResourceBindings": {
 "title": "text-firstName"
 },
 ... //etc
}

```
With resource texts:

```
...
{
 "id": "text-firstName",
 "value": "First name"
}

``
The error message would then be"You have to fill out First name"`.

Example: Component with shortName

If the field’s prompt is long or not suitable for use in the validation message, you can add a shortName text that can be used instead.
Note that this only applies to this specific validation message - the shortName text is not used otherwise in the solution as of now.

```
{
 "id": "firstName",
 "type": "Input",
 "textResourceBindings": {
 "title": "text-firstName",
 "shortName": "firstName-short",
 },
 ... //etc
}

```
With resource texts:

```
...
{
 "id": "text-firstName",
 "value": "Please type your first name in the field below:"
},
{
 "id": "firstName-short",
 "value": "your first name"
}

``
The error message would then be"You have to fill out your first name"`.

Custom error messages

It is possible to define custom error messages that will be displayed when a field doesn’t pass the validation check. This is done by including a parameter errorMessage where the field is defined in the JSON schema.
The JSON schema file is in the folder App/models and has a naming patterns as follows; *.schema.json,

An example of how to extend the example previously presented with a custom error message:

```
"someField": {
 "type": "string",
 "maxLength": "4",
 "errorMessage": "myCustomError"
}

```
The error text can be included directly. To enable language support, add a text key for a text defined in the resource files.

Notice that if you have a reference to a definition the error message must be added to the property-field and not the reference/definition.
Example:

```
{
 "properties": {
 "person": {
 "$ref" : "#/definitions/personDefinition",
 "errorMessage": "myCustomError",
 }
 },
 "definitions": {
 "personDefinition" : {
 "age": {
 "type": "number"
 },
 ...
 }
}

```
Note that when the XSD is changed, the custom error messages will de removed from the JSON schema.
In the future, there will be support for setting custom error messages in the data modelling tool in Altinn Studio. But for now, this is a manual job.Server-side validation

Server-side validation can be split into two categories:

Validations against data model - These run automatically whenever the user attempts to submit form data.

Custom validations - these are written by the application developer,
and run when the user attempts to submit form data or move the process to a new step.

How to add custom validation

Custom validation can also be split into two categories; task-validation and data-validation.

Task-validation will run each time validation is triggered either manually from the application or when you attempt to move forward in the process.

Data-validation will run if you’re on a step that has defined data elements associated with it.

Validations are written i C# and depending on the version of the application template and Nuget packages you are using,
the way the implementation is done varies slightly. In the earlier versions it’s a pre-created file where you put your
logic, while from version 7 and onwards you implement an interface in whatever class you like. The interface happens to
be equal to the pre-defined class in the earlier versions. The examples below which referrers to the methods to add your
validation logic to is the same.

v7In version 7 the way to do custom code instantiation has changed. We now use an dependency injection based approach
instead of overriding methods. If you previously used to place your custom code in the ValidateData and ValidateTask
methods in the ValidationHandler.cs class you will see that it’s mostly the same.

Create a class that implements the IInstanceValidator interface found in the Altinn.App.Core.Features.Validation namespace.
You can name and place the file in any folder you like within your project, but we suggest you use meaningful namespaces like in any other .Net project.

Register you custom implementation in the Program.cs class
```
services.AddTransient();

``
This ensures your custom code is known to the application and that it will be executed.
v4, v5, v6
Validations should be added to theValidationHandler.cs-file in the application template.
The file can be accessed and edited in Altinn Studio through the logic menu, by selecting *Rediger valideringer*,
or directly in the application repo where the file is under thelogic/Validation`-folder.From here on the examples should be valid for all versions:)

Custom logic are added to the ValidateData and ValidateTask-methods.
The former takes in a data object and the latter takes in the instance and taskId.
To add a validation error, the AddModelError-method of the validationResult-object, which is a parameter in both methods, is used.

An example of a simple data validation that tests that the field FirstName does not contain the value 1337, when the root element of the model is Skjema is shown below:

```
public void ValidateData(object data, ModelStateDictionary validationResults)
{
 if (data.GetType() == typeof(Skjema))
 {
 // Cast instance data to model type
 Skjema model = (Skjema)data;

// Get value to test - FirstName
 string firstName = Skjema?.Person?.FirstName;

// Check if FirstName exists, and contains the value "1337"
 if (firstName != null && firstName.Contains("1337"))
 {
 // Add validation error, with error message and list
 // of affected fields (in this case Person.FirstName)
 validationResults.AddModelError(
 "Person.FirstName",
 "Error: First name cannot contain the value '1337'."
 );
 }
 }
}

```
See comments in code above for an explanation of what the different parts do.

In the other parameter of the method AddModelError, where it says “Error: First name cannot contain the value '
1337’”, you can use a text key for a text defined in the resource files for multilingual support.

An example of a simple task validation that checks how long the user spent on Task_1 and returns an error if there has gone more than three days:

```
public async Task ValidateTask(Instance instance, string taskId, ModelStateDictionary validationResults)
{
 if (taskId.Equals("Task_1"))
 {
 DateTime deadline = ((DateTime)instance.Created).AddDays(3);
 if (DateTime.UtcNow < deadline)
 {
 validationResults.AddModelError("Task_1", $"Completion of Task_1 has taken too long. Please start over.");
 }
 }
}

```
Single field validation

If there is a need for immediate validation of a field
that can not be covered in the client side validation,
you can set up a trigger for validation on single fields in formLayout.json

NOTE: Trigger for validation on single fields in Stateless apps is not currently supported.
```
{
 "data": {
 "layout": [
 {
 "id": "3611fb2a-c06b-4fa7-a400-3f6c1ece64e1",
 "textResourceBindings": {
 "title": "25795.OppgavegiverNavnPreutfyltdatadef25795.Label"
 },
 "dataModelBindings": {
 "simpleBinding": "etatid"
 },
 "type": "Input",
 "triggers": ["validation"] , // <--- Add this field
 },
 {
 "id": "9ec368da-d6a9-4fbd-94d0-b4dfa8891981",
 "type": "Button",
 "textResourceBindings": {
 "title": "Button"
 },
 "dataModelBindings": {},
 "textResourceId": "Standard.Button.Button",
 "customType": "Standard"
 }
 ]
 }
}

``
Note that if you define a field to trigger validation server-side, only the result of this validation will be displayed. Meaning,
if there is another client-side validation defined, a possible server-side validation of the field will overwrite these. Therefore, you should make sure
to implement all necessary validations on the server-side as well. It is possible to attach multiple error messages to the same field if needed.The configuration above will result in your own custom validation inValidationHandler.cs`
being triggered each time the field is updated. If you need to know which field
triggered the validation, this is available in the http-context as a header of the request named ValidationTriggerField.

An example of a custom validation where the header value is retrieved is shown below.

```
 public async Task ValidateData(object data, ModelStateDictionary validationResults)
 {
 _httpContextAccessor.HttpContext
 .Request.Headers
 .TryGetValue("ValidationTriggerField", out StringValues triggerValues);

string triggerField = triggerValues.FirstOrDefault(string.Empty);

if (triggerField.Equals("kommune"))
 {
 // Cast instance data to model type
 flyttemelding model = (flyttemelding)data;

// Get value to test - Kommune
 string kommune = model.kommune;

if (!kommune.Equals("Oslo"))
 {
 validationResults.AddModelError(triggerField, "This is not a valid municipality.");
 }
 }

await Task.CompletedTask;
 }

```
NOTE validation of single fields should be implemented in a way where it is both run on triggers and during general validation.
The example that revolves multiple complex validations show how this can be implemented.

Several things has been done to get this code to run

In ValidationHandler.cs using Microsoft.Extensions.Primitives; is included at the top of the file to be able to use StringValues.

In App.cs using Microsoft.AspNetCore.Http; is included at the top of the file to be able to use IHttpContextAccessor.

In App.cs IHttpContextAccessor is dependency injected in the constructor and passed along to ValidationHandler.

```
public App(
 IAppResources appResourcesService,
 ILogger logger,
 IData dataService,
 IProcess processService,
 IPDF pdfService,
 IProfile profileService,
 IRegister registerService,
 IPrefill prefillService,
 IHttpContextAccessor httpContextAccessor // <--- Add this line
 ) : base(appResourcesService, logger, dataService, processService, pdfService, prefillService)
 {
 _logger = logger;
 _validationHandler = new ValidationHandler(httpContextAccessor); // <--- Include the new property here
 _calculationHandler = new CalculationHandler();
 _instantiationHandler = new InstantiationHandler(profileService, registerService);
 }

```
If there are multiple complex validations that are time consuming, it is recommended to implement several private methods
to validate these and use ValidationTriggerField to determine which private method is to be run.
You can e.g. use a switch statement to accomplish this.

```
public async Task ValidateData(object data, ModelStateDictionary validationResults)
{
 if (data is flyttemelding model)
 {
 _httpContextAccessor.HttpContext
 .Request.Headers
 .TryGetValue("ValidationTriggerField", out StringValues triggerValues);

string triggerField = triggerValues.FirstOrDefault(string.Empty);

switch (triggerField)
 {
 case "kommune":
 ValidateKommune(model, validationResults);
 break;
 case "boaddresse":
 ValidateBoAdresse(model, validationResults);
 break;
 default:
 ValidateKommune(model, validationResults);
 ValidateBoAdresse(model, validationResults);
 break;
 }
 }
}

private void ValidateKommune(flyttemelding model, ModelStateDictionary validationResults)
{
 if (model.kommune != null && !model.kommune.Equals("Oslo"))
 {
 validationResults.AddModelError(
 nameof(model.kommune), 
 "This is not a valid municipality.");
 }
}
private void ValidateBoAdresse(flyttemelding model, ModelStateDictionary validationResults)
{
 if (model.boaddresse != null && model.boaddresse.Length > 150)
 {
 validationResults.AddModelError(
 nameof(model.boaddresse), 
 "Address can not be longer than 150 characters.");
 }
}

```

Specify that validation errors are fixed

When validation is triggered by a single field, all former validations on this field will be removed pending a response from the last validation.
If a field triggers validation that updates/adds an error message to multiple fields at once, these will not be removed even when there no longer are any
errors in these fields. This is because there is no way to know which fields may have been validated through a single field validation.

For example, if you have two fields; first name and last name. Both fields trigger single field validation, and if both fields have a value, you can validate that
the full name can not be longer than 50 characters. An error message is then set on both fields. If you correct this by changing the first name, the error message from first name will
disappear, but the error message on the last name field will still be displayed even though the validation does not set any error messages on the fields.

```
private void ValidateFullName(Datamodell model, ModelStateDictionary validationResults)
{
 if (!string.isNullOrEmpty(model.fornavn) && !string.isNullOrEmpty(model.etternavn)
 && model.fornavn.Length + model.etternavn.Length > 50)
 {
 validationResults.addModelError(nameof(model.fornavn),
 "Full name can not be longer than 50 characters.");
 validationResults.addModelError(nameof(model.etternavn),
 "Full name can not be longer than 50 characters.");
 }
}

```
To be able to remove old error messages in a case like this, there has been added support to be able to specify that a validation error has been fixed.
Then, the field in question will be able to be notified that a specific error message that it is displaying has been fixed and can now be hidden.

This is done by adding a validation error in the code in the case where there are no errors in the validation,
and set *FIXED* in front of the error message itself. This corresponds to the setup for soft validation.
This prefix causes the error message that is set to be removed from the field in question, or ignored (if there is no error message on the field already).

You can now expand the example above to support this:

```
private void ValidateFullName(Datamodell model, ModelStateDictionary validationResults)
{
 if (!string.isNullOrEmpty(model.fornavn) && !string.isNullOrEmpty(model.etternavn)
 && model.fornavn.Length + model.etternavn.Length > 50)
 {
 validationResults.addModelError(nameof(model.fornavn),
 "Full name can not be longer than 50 characters.");
 validationResults.addModelError(nameof(model.etternavn),
 "Full name can not be longer than 50 characters.");
 } 
 else
 {
 validationResults.addModelError(nameof(model.fornavn),
 "*FIXED*Full name can not be longer than 50 characters.");
 validationResults.addModelError(nameof(model.etternavn),
 "*FIXED*Full name can not be longer than 50 characters.");
 }
}

Soft validations

Soft validations are validation messages that does not stop the user from submitting or move onto the next step of the process, but that are used to give the user different forms of information.
These types of validations can for example be used to ask the user to verify input that seems wrong or strange, but which strictly speaking is not invalid, or give useful information for further filling out the form.

Messages based on soft validation will be displayed once, but the user can choose to move on without making any changes.

Soft validations are added from the server-side the application logic, in the same way as regular validation errors. The difference is that the validation message
must be prefixed with the type of validation you want to give, e.g. *WARNING*. This will be interpreted as a soft validation. The prefix *WARNING* will not be displayed for the user.

The different types of soft validations are WARNING, INFO and SUCCESS.

Code example

```
public async Task ValidateData(object data, ModelStateDictionary modelState)
{
 if (data is TestModel testModel)
 {
 string firstName = testModel?.Person?.FirstName;
 if (firstName != null && firstName.Contains("1337")) 
 {
 validationResults.AddModelError(
 "Person.FirstName", 
 "*WARNING*Are you sure your first name contains 1337?");
 }

if (firstName != null && firstname.Contains("Altinn"))
 {
 validationResults.AddModelError(
 "Person.FirstName", 
 "*SUCCESS*Altinn is a great name!");
 }
 }

await Task.CompletedTask;
}

```
Examples on display of different validations below:

Group validation

It is possible to apply validations to a repeating group when the user saves a row in the group.
This can be done by adding a trigger on the group component in the layout file (e.g. FormLayout.json).
There are two different triggers that can be used for groups; validation runs validation on the entire group,
and validateRow only runs validation on the row the user is trying to save. Example:

```
{
 "data": {
 "layout": [
 {
 "id": "demo-gruppe",
 "type": "Group",
 "children": [
 "..."
 ],
 "maxCount": 3,
 "dataModelBindings": {
 "group": "Endringsmelding-grp-9786.OversiktOverEndringene-grp-9788"
 },
 "triggers": ["validateRow"] // <--- Add this
 },
 ...
 ]
 }
}

```
This will ensure that validation is run on the components that are a part of the group in the row you’re working on.
If there are validation errors you will be stopped from saving the group until this has been corrected.

If you add validation on the group component, a call will be made towards the validation back-end with a header specifying which component triggered the validation: ComponentId.
Additionally, the row index of the row being saved is available in the header RowIndex. If the group is a nested group, a comma separated list of row indices is returned, otherwise it is a single number.
Validations are written in C# in the ValidationHandler.cs-file in the application template. In the validation, you can retrieve component id and tailor possible validations to run in the back-end, example:

```
public async Task ValidateData(object data, ModelStateDictionary validationResults)
{
 if (data is flyttemelding model)
 {
 _httpContextAccessor.HttpContext
 .Request.Headers
 .TryGetValue("ComponentId", out StringValues compIdValues);

_httpContextAccessor.HttpContext
 .Request.Headers
 .TryGetValue("RowIndex", out StringValues rowIndexValues);

string componentId = compIdValues.FirstOrDefault(string.Empty);

switch (componentId)
 {
 case "top-level-group":
 // run validations specific to the group

// Get row index for a non-nested group
 int rowIndex = int.Parse(rowIndexValues.FirstOrDefault(string.Empty));

break;
 case "nested-group":
 // Get all row indices for a nested group
 int[] rowIndices = rowIndexValues
 .FirstOrDefault(string.Empty)
 .Split(",", StringSplitOptions.RemoveEmptyEntries)
 .Select(s => int.Parse(s))
 .ToArray();

break;
 default:
 // run the validations in their entirety
 break;
 }
 }
}

```
For tips on how you solve complex validations, see the examples under single field validation.
Human: is it possible to group fields together?[0m

[1m> Finished chain.[0m

[1m> Finished chain.[0m
stuff chain response:
('Yes, it is possible to group fields together in a form. This can be done '
 'using the Group component in the layout configuration. The Group component '
 'allows you to visually group related fields together and apply specific '
 'settings or behaviors to the group as a whole.\n'
 '\n'
 'To create a group, you need to define the Group component in the layout '
 'configuration and specify the child components that should be included in '
 'the group. Here is an example of how a Group component can be defined:\n'
 '\n'
 '```\n'
 '{\n'
 '  "id": "my-group",\n'
 '  "type": "Group",\n'
 '  "children": [\n'
 '    "field1",\n'
 '    "field2",\n'
 '    "field3"\n'
 '  ]\n'
 '}\n'
 '```\n'
 '\n'
 'In this example, "field1", "field2", and "field3" are the IDs of the child '
 'components that should be included in the group.\n'
 '\n'
 'You can also configure additional settings for the group, such as the title '
 'or appearance. For example:\n'
 '\n'
 '```\n'
 '{\n'
 '  "id": "my-group",\n'
 '  "type": "Group",\n'
 '  "children": [\n'
 '    "field1",\n'
 '    "field2",\n'
 '    "field3"\n'
 '  ],\n'
 '  "textResourceBindings": {\n'
 '    "title": "Group Title"\n'
 '  },\n'
 '  "panel": {\n'
 '    "variant": "info"\n'
 '  }\n'
 '}\n'
 '```\n'
 '\n'
 'In this example, the group has a title of "Group Title" and is displayed as '
 'an info panel.\n'
 '\n'
 'By grouping fields together, you can improve the organization and '
 'readability of your form, making it easier for users to understand and fill '
 'out the required information.')
Time to retrieve response: 18.28847437503282 seconds

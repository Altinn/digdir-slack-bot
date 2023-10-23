ExtractedSearchTerms(searchTerms=['expressions', 'text field', 'value', 'at least', '3 characters'])
Unique URLs
['https://docs.altinn.studio/altinn-studio/designer/build-app/expressions/']


[1m> Entering new StuffDocumentsChain chain...[0m


[1m> Entering new LLMChain chain...[0m
Prompt after formatting:
[32;1m[1;3mSystem: Use the following pieces of context to answer the users question. 
If you don't know the answer, just say that you don't know, don't try to make up an answer.
----------------
Build Expressions in Altinn Studio

How to build expressions with Altinn Studio.

This documentation will describe how to build expressions connected to component fields using the Expressions tool in
Altinn Studio.

Expressions are a concept in Altinn apps that lets app-developers dynamically assign values to different elements in an
application. Please read more in
the Expressions section of Apps documentation of what expressions can be
used for and how the syntax works.

Terminology

In Altinn Studio the concept is called logic where an expression is addressed as a logic rule.

Expression: A unit consisting of the boolean component field and the actual expression that will evaluate to be a
boolean value when calculated in a running app. The most simple expression can consist of a single sub expression,
while a more advanced expression can consist of multiple sub expressions combined with an operator.

Sub Expression: A term used to address the most elementary unit of an expression that only consists of a
function and two values, whereas a value either can be a single element or a combined element with the first part of
the element defining a source where the following value can be found.

Property or Field: The boolean property or field of the component that the expression should be connected to.

Function: The function that should be used to compare the two values in the sub expression.

Data Source: The source for the values in the sub expression. Can also be addressed as the type of the value.

Data Source Value: The actual value that should be used to evaluate the sub expression. However, if the value has
a
data source being application settings, component, data model or instance context, it acts as a reference to a
value rather than an explicit value.

Operator: The operator will only be relevant when there are more than one sub expression and will be used to
evaluate if all the sub expressions should imply (use AND) or if it is enough that only one of the sub
expressions
implies (use OR).

Building expressions in Altinn Studio

When building expressions in the Expressions panel in Studio, it is always possible to add one expression for each of the following states:

hidden

required

readOnly

For group components, also these states can have attached expressions:

edit.addButton

edit.deleteButton

edit.saveButton

edit.saveAndNextButton

If all these fields have expressions added to them you will be shown an info message saying that you have reached the limit for
expressions.

when going forward configuring an expression for your component in the Expression tool in Altinn Studio for the first
time, follow this guide:

Basic Expressions

Choose a component field to add the expression to

2. Choose a function that you want your first sub expression to use

3. Choose a data source that you want the first element in your sub expression to be

This data source can be either an actual source which will provide you with a set of available values to choose
from, or the data source can be a type for a value. The available data sources that will provide you with a set of
given values are:

WARNING: The given values provided when choosing Application Settings as the data source are not yet implemented.
4. Choose a value that you want the first element in your sub expression to have

WARNING: The given values provided when choosing Application Settings as the data source are not yet implemented.
4. Choose a value that you want the first element in your sub expression to have

5. Choose a comparable data source and value for the second element in your sub expression

6. Save expression or continue adding sub expressions

Saving the expression will connect the expression to the component property you chose and visualize it in a preview
mode.

Or you can keep adding sub expression by expanding the rule and set the operator, that should evaluate the sub
expressions together, to either and or or.

Then you repeat these steps from point 2 - adding a function to the new sub expression and so on.

Then you can save the complete expression, with the arbitrary number of sub expressions, and visualize it in preview
mode.

“Complex” expressions

There is also a possibility for adding expressions by writing them directly in the syntax expected by the configuration
of a running Altinn app. This functionality will be enabled in Studio if the expression is
manually added to the field through Gitea or an editor IDE and if the expression is written in a way that can not be
interpreted by the Studio Expressions tool. This accounts for nested expressions, as well as for expressions
that are written in a simplified way, e.g. not including the function, since it will be interpreted by app-frontend
implicitly.

The possibility to edit the expression by freestyle writing can also be enabled as an option at any given point.
However, when editing the expression freestyle you will only be able to switch back to using the Studio tool if you
write an expression that can be interpreted by the tool.

See that the switch is available to enable freestyle editing:

Enable it and see your expression in the freestyle editing text area:

Making changes to an invalid (or not-interpretable) expression will disable the switch:

Limitations

As mentioned there are a few limitations in the Studio tool for configuring expressions.

Available Component Fields

Firstly, there are only some component fields that Studio are able to interpret and build connected
expressions for. In a later stage of development we will enable building and interpreting expressions connected to

text resource bindings on components

process

Nesting

Second, Studio is limited to building expressions with only one level of nesting. This means that a value in a sub
expression only can be either an implicit or explicit value and not a sub expression. If the value is a sub expression
you will end up with a “complex” expression as in the example above.

Existing Boolean properties are lost when adding expressions

If you have defined any of the boolean properties/fields on the component to have a boolean value, true or false,
and you connect an expression to it, Studio will not remember this value. This means that if you add an expression to a
field that originally had a boolean value and you delete the expression, the field will disappear from the component and
be evaluated to its default value.

What is a Valid Expression from a Studio Point of View

To be allowed to save an expression to the layout file Studio will only visualize the Save button when some
conditions
imply:

You have selected a component property/field that the expression should be connected to

You have selected a function for the first sub expression of your expression

When these conditions imply you can save the expression without filling in any of the values. This will add an
expression looking like this to the given component field:

```
"[COMPONENT_PROPERTY]": [
"[FUNCTION]",
null,
null
]

``
Be aware that the expression will be valid and calculate a boolean value that will have effect on the behaviour of your
component. Depending on the chosen function the expression can be calculated totrueorfalse. If thenullvalues
would not make sense with the given function the default calculated expression value will befalse`.
Human: how can I use expressions to make sure that a text field has a value that is at least 3 characters?[0m

[1m> Finished chain.[0m

[1m> Finished chain.[0m
stuff chain response:
('To ensure that a text field has a value that is at least 3 characters using '
 'expressions in Altinn Studio, you can follow these steps:\n'
 '\n'
 '1. Choose the text field component that you want to add the expression to.\n'
 '2. Select the "required" state for the component.\n'
 '3. Choose the function "length" for the sub expression.\n'
 '4. Choose the data source "component" for the first element in the sub '
 'expression.\n'
 '5. Select the text field component as the value for the first element.\n'
 '6. Choose the comparable data source "value" for the second element in the '
 'sub expression.\n'
 '7. Enter the value "3" as the minimum length for the text field.\n'
 '8. Save the expression.\n'
 '\n'
 'This expression will ensure that the text field is required and will only be '
 'considered valid if it has a value with a length of at least 3 characters.')
Time to retrieve response: 12.373695000016596 seconds

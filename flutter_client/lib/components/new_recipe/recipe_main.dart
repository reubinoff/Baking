import 'package:flutter/material.dart';

class RecipeMainForm extends StatefulWidget {
  const RecipeMainForm({
    Key? key,
  }) : super(key: key);

  @override
  RecipeMainFormState createState() {
    return RecipeMainFormState();
  }
}

class RecipeMainFormState extends State<RecipeMainForm> {
  final _formKey = GlobalKey<FormState>();

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('New Recipe'),
      ),
      body: Form(
        key: _formKey,
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: <Widget>[
            TextFormField(
              decoration: const InputDecoration(
                hintText: 'Enter recipe name',
              ),
              validator: (value) {
                if (value == null || value.isEmpty) {
                  return 'Please enter some text';
                }
                return null;
              },
            ),
            const Padding(
              padding: EdgeInsets.symmetric(vertical: 16.0),
              child: ElevatedButton(
                onPressed: null,
                child: Text('Next'),
              ),
            ),
          ],
        ),
      ),
    );
  }
}

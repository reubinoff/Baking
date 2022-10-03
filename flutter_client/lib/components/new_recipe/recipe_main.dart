import 'package:baking_client/components/new_recipe/new_procedure.dart';
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
      body: _buildForm(),
    );
    return Form(
      key: _formKey,
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Padding(
              padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 16),
              child: TextFormField(
                decoration: const InputDecoration(
                  border: UnderlineInputBorder(),
                  labelText: 'Enter your recipe name',
                ),
                autofocus: true,
                validator: (value) {
                  if (value == null || value.isEmpty) {
                    return 'We must have it';
                  }
                  return null;
                },
              )),
          Padding(
              padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 16),
              child: TextFormField(
                maxLines: 3,
                decoration: const InputDecoration(
                  border: UnderlineInputBorder(),
                  labelText: 'Enter your recipe description',
                ),
                validator: (value) {
                  if (value == null || value.isEmpty) {
                    return 'Give us Some information';
                  }
                  return null;
                },
              )),
          Padding(
            padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 16.0),
            child: ElevatedButton(
              onPressed: () {
                // Open NewProcedure Form
                Navigator.push(
                  context,
                  MaterialPageRoute(builder: (context) => const NewProcedure()),
                );
              },
              child: const Text('Submit'),
            ),
          ),
        ],
      ),
    );
  }
}

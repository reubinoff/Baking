import 'package:baking_client/components/new_recipe/recipe_main.dart';
import 'package:flutter/material.dart';

class NewRecipeRoute extends StatelessWidget {
  const NewRecipeRoute({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('New Recipe'),
        centerTitle: false,
      ),
      body: const RecipeMainForm(),
      // body: Center(
      //   child: ElevatedButton(
      //     onPressed: () {
      //       Navigator.pop(context);
      //     },
      //     child: const Text('Go back!'),
      //   ),
      // ),
    );
  }
}

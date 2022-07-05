import 'package:baking_client/components/image_stack.dart';
import 'package:baking_client/models/recipe.dart';
import 'package:flutter/material.dart';

class RecipeViewFull extends StatelessWidget {
  const RecipeViewFull({Key? key, required this.recipe}) : super(key: key);
  final Recipe recipe;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(recipe.name),
        centerTitle: false,
      ),
      body: Column(
        children: <Widget>[
          Expanded(
            child: RecipeImage(cdnUrl: recipe.cdnUrl ?? ''),
          ),
        ],
      ),
    );
  }
}

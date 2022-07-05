import 'package:baking_client/models/recipe.dart';
import 'package:flutter/material.dart';

class RecipeViewFull extends StatefulWidget {
  const RecipeViewFull({Key? key, required this.recipe}) : super(key: key);

  final Recipe recipe;

  @override
  _RecipeViewState createState() => _RecipeViewState();
}

class _RecipeViewState extends State<RecipeViewFull> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(widget.recipe.name),
        centerTitle: false,
      ),
      body: const Center(
        child: Text('Recipe View'),
      ),
    );
  }
}

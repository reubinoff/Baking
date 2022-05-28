import 'package:baking_client/recipe_view.dart';
import 'package:flutter/material.dart';

class HomePage extends StatelessWidget {
  const HomePage({
    required this.title,
    Key? key,
  }) : super(key: key);
  final String title;
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(title),
        actions: [
          IconButton(
            icon: const Icon(Icons.search),
            tooltip: 'Search for recipe',
            onPressed: () {},
          ),
          IconButton(
            icon: const Icon(Icons.add),
            tooltip: 'Add new Recipe',
            onPressed: () {},
          ),
        ],
      ),
      body: const RecipeView(),
    );
  }
}

import 'dart:math';

import 'package:baking_client/models/recipe.dart';
import 'package:flutter/material.dart';

class RecipeCard extends StatelessWidget {
  const RecipeCard({
    Key? key,
    required this.recipe,
  }) : super(key: key);

  final Recipe recipe;

  @override
  Widget build(BuildContext context) {
    return Container(
      child: getCard(context),
    );
  }

  Card getCard(BuildContext context) {
    var ran = Random();
    final cardImage = NetworkImage(
        'https://source.unsplash.com/random/800x600?house&' +
            ran.nextInt(100).toString());
    return Card(
        elevation: 4.0,
        child: Column(
          children: [
            ListTile(
                title: Text(recipe.name),
                // subtitle: Text(recipe.description),
                trailing: SizedBox(
                  child: Chip(
                    backgroundColor: Colors.transparent,
                    avatar: const CircleAvatar(
                      backgroundColor: Colors.transparent,
                      child: IconTheme(
                        data: IconThemeData(color: Colors.blue),
                        child: Icon(Icons.water),
                      ),
                    ),
                    label: Text(recipe.hydration.toString() + "%"),
                  ),
                )),
            SizedBox(
              height: 200.0,
              child: Ink.image(
                image: cardImage,
                fit: BoxFit.cover,
              ),
            ),
            Container(
              padding: const EdgeInsets.all(16.0),
              alignment: Alignment.centerLeft,
              child: Text(recipe.description),
            ),
            ButtonBar(
              children: [
                TextButton(
                  child: const Text('BAKE'),
                  onPressed: () {/* ... */},
                ),
              ],
            )
          ],
        ));
  }
}

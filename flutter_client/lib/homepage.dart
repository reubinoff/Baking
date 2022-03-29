import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:baking_client/models/recipe.dart';
import 'package:http/http.dart' as http;

import 'components/recipe_card.dart';

class HomePage extends StatelessWidget {
  const HomePage({
    required this.title,
    Key? key,
  }) : super(key: key);

  final String api = "http://localhost:8888/recipe";
  final String title;

  List<Recipe> parseRecipe(String responseBody) {
    final parsed =
        jsonDecode(responseBody)["items"].cast<Map<String, dynamic>>();
    return parsed.map<Recipe>((json) => Recipe.fromJson(json)).toList();
  }

  Future<List<Recipe>> fetchData(http.Client client) async {
    final response = await client.get(Uri.parse(api), headers: {
      "Accept": "application/json",
      "Access-Control_Allow_Origin": "*"
    });
    if (response.statusCode == 200) {
      return parseRecipe(response.body);
    } else {
      throw Exception('Failed to load recipe');
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(title),
      ),
      body: FutureBuilder<List<Recipe>>(
        future: fetchData(http.Client()),
        builder: (context, snapshot) {
          if (snapshot.hasError) {
            return const Center(
              child: Text('An error has occurred!'),
            );
          } else if (snapshot.hasData) {
            return RecipeList(recipes: snapshot.data!);
          } else {
            return const Center(
              child: CircularProgressIndicator(),
            );
          }
        },
      ),
    );
  }
}

class RecipeList extends StatelessWidget {
  const RecipeList({Key? key, required this.recipes}) : super(key: key);

  final List<Recipe> recipes;

  @override
  Widget build(BuildContext context) {
    return GridView.builder(
      gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
        crossAxisCount: 2,
      ),
      itemCount: recipes.length,
      itemBuilder: (BuildContext context, int index) {
        return Center(
          child: RecipeCard(recipe: recipes[index]),
        );
      },
    );
  }
}
/*
  const ListTile(
                            leading: Icon(Icons.album),
                            title: Text('The Enchanted Nightingale'),
                            subtitle: Text(
                                'Music by Julie Gable. Lyrics by Sidney Stein.'),
                          )
                          */
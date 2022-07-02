import 'package:baking_client/components/new_recipe/new_recipe_home.dart';
import 'package:baking_client/recipe_view.dart';
import 'package:flutter/material.dart';
import 'components/home_page_drawer.dart';
import 'components/recipe_search_delegate.dart';

class HomePage extends StatefulWidget {
  const HomePage({
    required this.title,
    Key? key,
  }) : super(key: key);
  final String title;

  @override
  State<HomePage> createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(widget.title),
        actions: [
          IconButton(
            icon: const Icon(Icons.search),
            tooltip: 'Search for recipe',
            onPressed: () {
              showSearch(context: context, delegate: RecipeSearchDelegate());
            },
          ),
          IconButton(
            icon: const Icon(Icons.add),
            tooltip: 'Add new Recipe',
            onPressed: () {
              Navigator.push(
                context,
                MaterialPageRoute(builder: (context) => const NewRecipeRoute()),
              );
            },
          ),
        ],
      ),
      drawer: const HomePageDrawer(),
      body: const RecipeView(
        showImage: true,
        query: "",
      ),
      // floatingActionButton: FloatingActionButton(
      //   onPressed: () {
      //     // Add your onPressed code here!
      //   },
      //   backgroundColor: Colors.green,
      //   child: const Icon(Icons.add),
      // ),
    );
  }
}

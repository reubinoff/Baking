import 'package:baking_client/services/recipes.dart';
import 'package:flutter/material.dart';

import 'models/recipe.dart';

import 'components/recipe_card.dart';

class RecipeView extends StatefulWidget {
  const RecipeView({
    Key? key,
  }) : super(key: key);

  @override
  _RecipeViewState createState() => _RecipeViewState();
}

class _RecipeViewState extends State<RecipeView> {
  RecipeNotifier notifier = RecipeNotifier();

  @override
  void initState() {
    super.initState();
    notifier.getMore();
  }

  @override
  void dispose() {
    notifier.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return ValueListenableBuilder<List<Recipe>>(
        valueListenable: notifier,
        builder: (BuildContext context, List<Recipe> value, Widget? child) {
          return value.isNotEmpty
              ? RefreshIndicator(
                  onRefresh: () async {
                    notifier.reload();
                  },
                  child: NotificationListener<ScrollNotification>(
                      onNotification: (ScrollNotification scrollInfo) {
                        if (scrollInfo is ScrollEndNotification &&
                            scrollInfo.metrics.extentAfter == 0) {
                          notifier.getMore();
                          return true;
                        }
                        return false;
                      },
                      child: RecipeList(recipes: value)),
                )
              : const Center(child: CircularProgressIndicator());
        });
  }
}

class RecipeList extends StatelessWidget {
  const RecipeList({Key? key, required this.recipes}) : super(key: key);

  final List<Recipe> recipes;

  @override
  Widget build(BuildContext context) {
    return GridView.builder(
      gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
        crossAxisCount: 1,
        crossAxisSpacing: 10,
        mainAxisSpacing: 10,
      ),
      padding: const EdgeInsets.all(16),
      itemCount: recipes.length,
      itemBuilder: (BuildContext context, int index) {
        return Center(
          child: RecipeCard(recipe: recipes[index]),
        );
      },
    );
  }
}

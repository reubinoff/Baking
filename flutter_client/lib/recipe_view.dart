import 'package:baking_client/services/recipes.dart';
import 'package:flutter/material.dart';

import 'models/recipe.dart';

import 'components/recipe_card.dart';

class RecipeView extends StatefulWidget {
  const RecipeView({
    Key? key,
    required this.showImage,
    required this.query,
  }) : super(key: key);

  final bool showImage;
  final String query;

  @override
  _RecipeViewState createState() => _RecipeViewState();
}

class _RecipeViewState extends State<RecipeView> {
  late RecipeNotifier notifier;

  @override
  void initState() {
    super.initState();
    // debugPrint("MOSHE >>>>>" + widget.query);
    notifier = RecipeNotifier(query: widget.query);
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
                      child: RecipeList(
                          recipes: value, showImage: widget.showImage)),
                )
              : notifier.loading
                  ? const Center(child: CircularProgressIndicator())
                  : const Center(child: Text("No recipes found"));
        });
  }
}

class RecipeList extends StatelessWidget {
  const RecipeList({Key? key, required this.recipes, required this.showImage})
      : super(key: key);

  final List<Recipe> recipes;
  final bool showImage;
  @override
  Widget build(BuildContext context) {
    return ListView.separated(
      padding: const EdgeInsets.all(10),
      itemCount: recipes.length,
      separatorBuilder: (BuildContext context, int index) => const Divider(),
      itemBuilder: (BuildContext context, int index) {
        final Recipe recipe = recipes[index];
        return RecipeCard(recipe: recipe, showImage: showImage);
      },
    );
  }
}

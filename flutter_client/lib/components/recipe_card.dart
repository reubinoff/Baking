import 'package:baking_client/components/image_stack.dart';
import 'package:baking_client/components/recipe_view/recipe_view_main.dart';
import 'package:baking_client/models/recipe.dart';
import 'package:flutter/material.dart';

class RecipeCard extends StatelessWidget {
  const RecipeCard({
    Key? key,
    required this.recipe,
    required this.showImage,
  }) : super(key: key);

  final Recipe recipe;
  final bool showImage;

  @override
  Widget build(BuildContext context) {
    return Container(
      child: getCard(context),
    );
  }

  InkWell getCard(BuildContext context) {
    return InkWell(
      onTap: () {
        Navigator.push(
          context,
          MaterialPageRoute(
            builder: (context) => RecipeViewFull(
              recipe: recipe,
            ),
          ),
        );
      },
      child: Card(
          elevation: 15.0,
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(15),
          ),
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
              showImage
                  ? SizedBox(
                      height: 200.0, child: RecipeImage(cdnUrl: recipe.cdnUrl))
                  : Container(),
              Container(
                padding: const EdgeInsets.all(16.0),
                alignment: Alignment.centerLeft,
                child: Text(recipe.description),
              ),
            ],
          )),
    );
  }
}

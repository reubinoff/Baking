import 'package:baking_client/components/recipe_view/recipe_view_main.dart';
import 'package:baking_client/models/recipe.dart';
import 'package:flutter/material.dart';
import 'package:transparent_image/transparent_image.dart';

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

  _getImage(BuildContext context) {
    if (recipe.cdnUrl == null || recipe.cdnUrl!.isEmpty) {
      return Stack(children: <Widget>[
        Center(
            child: Ink.image(
          image: const AssetImage('assets/images/bread_placeholder.jpeg'),
          fit: BoxFit.cover,
        ))
      ]);
    } else {
      final FadeInImage breadImage = FadeInImage.memoryNetwork(
        placeholder: kTransparentImage,
        image: recipe.cdnUrl ?? '',
        fit: BoxFit.cover,
      );

      return Stack(
        children: <Widget>[
          const Center(child: CircularProgressIndicator()),
          SizedBox(
            width: MediaQuery.of(context).size.width,
            height: MediaQuery.of(context).size.height,
            child: breadImage,
          )
        ],
      );
    }
  }

  Card getCard(BuildContext context) {
    return Card(
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
                ? SizedBox(height: 200.0, child: _getImage(context))
                : Container(),
            Container(
              padding: const EdgeInsets.all(16.0),
              alignment: Alignment.centerLeft,
              child: Text(recipe.description),
            ),
            ButtonBar(
              children: [
                TextButton(
                  child: const Text('BAKE'),
                  onPressed: () {
                    Navigator.push(
                      context,
                      MaterialPageRoute(
                          builder: (context) => RecipeViewFull(recipe: recipe)),
                    );
                  },
                ),
              ],
            )
          ],
        ));
  }
}

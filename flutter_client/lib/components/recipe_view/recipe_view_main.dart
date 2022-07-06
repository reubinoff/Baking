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
      body: CustomScrollView(
        slivers: <Widget>[
          SliverList(
            delegate: SliverChildListDelegate(
              [
                SizedBox(
                    height: 200.0,
                    child: Expanded(
                        child: RecipeImage(cdnUrl: recipe.cdnUrl ?? ''))),
                const SizedBox(height: 16),
                Text(
                  recipe.name,
                  style: Theme.of(context).textTheme.headline6,
                ),
                const SizedBox(height: 16),
                Text(
                  recipe.description,
                  style: Theme.of(context).textTheme.bodyText1,
                ),
                const SizedBox(height: 16),
                Text(
                  'Ingredients',
                  style: Theme.of(context).textTheme.headline6,
                ),
                const SizedBox(height: 16),
                Text(
                  'Steps',
                  style: Theme.of(context).textTheme.headline6,
                ),
                const SizedBox(height: 16),
              ],
            ),
          ),
        ],
      ),
    );
  }
}


//  Column(
//         children: <Widget>[
//           SizedBox(
//               height: 200.0,
//               child: Expanded(child: RecipeImage(cdnUrl: recipe.cdnUrl ?? ''))),
//         ],
//       ),
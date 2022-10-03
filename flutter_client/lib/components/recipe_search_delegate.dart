import 'package:baking_client/recipe_view.dart';
import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';

class RecipeSearchDelegate extends SearchDelegate<String> {
  static const int totalInRecentSearch = 10;
  @override
  List<Widget> buildActions(BuildContext context) {
    return [
      IconButton(
        icon: const Icon(Icons.clear),
        onPressed: () {
          query = '';
        },
      ),
    ];
  }

  @override
  Widget buildLeading(BuildContext context) {
    return IconButton(
      icon: AnimatedIcon(
        icon: AnimatedIcons.menu_arrow,
        progress: transitionAnimation,
      ),
      onPressed: () {
        close(context, "");
      },
    );
  }

  @override
  Widget buildResults(BuildContext context) {
    debugPrint("buildResults for $query");
    saveQuery(query);
    return RecipeView(
      showImage: false,
      query: query,
    );
  }

  @override
  Widget buildSuggestions(BuildContext context) {
    final suggestions = _buildSuggestion(query);

    return suggestions;
  }

  Widget _buildSuggestion(String queryStr) {
    return FutureBuilder<List<String>?>(
      future: SharedPreferences.getInstance()
          .then((prefs) => prefs.getStringList('search_items')),
      builder: (context, snapshot) {
        // debugPrint(snapshot.data.toString());
        if (snapshot.hasData) {
          return ListView.builder(
            itemCount: snapshot.data?.length,
            itemBuilder: (context, index) {
              if (snapshot.data![index].contains(queryStr)) {
                return ListTile(
                  title: Text(snapshot.data![index]),
                  onTap: () {
                    query = snapshot.data![index];
                    showResults(context);
                  },
                );
              } else {
                return Container();
              }
            },
          );
        } else {
          debugPrint('No data');
          return const Center();
        }
      },
    );
  }

  saveQuery(String queryStr) async {
    queryStr.trim();
    if (queryStr.isEmpty) return;
    SharedPreferences prefs = await SharedPreferences.getInstance();
    List<String> searchItems = prefs.getStringList('search_items') ?? [];
    if (searchItems.contains(queryStr)) {
      searchItems.removeWhere((element) => element == queryStr);
    }
    searchItems.insert(0, queryStr);
    searchItems.length = searchItems.length > totalInRecentSearch
        ? totalInRecentSearch
        : searchItems.length;
    prefs.setStringList('search_items', searchItems);
  }
}

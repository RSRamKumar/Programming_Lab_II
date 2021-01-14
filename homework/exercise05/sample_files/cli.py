import click

from oop_nx import Network, Analyzer, Statistics


@click.group()
def main():
    """Entry method."""
    pass


@main.command()
@click.argument('ppi')
@click.argument('nodes')
@click.argument('edges')
@click.option('-r', '--enrich', default=False, is_flag=True, help="Enrich the graph with RNA and DNA molecules.")
def compile(ppi: str, nodes: str, edges: str, enrich: bool):
    """Generates node/edge lists from a PPI file."""
    network = Network(ppi_file=ppi, enrich=enrich)
    network.compile_files(node_file_path=nodes, edge_file_path=edges)


@main.command()
@click.option('-p', '--ppi', default=None, help="A CSV file containing PPIs.")
@click.option('-n', '--nodes', default=None, help="A TSV file containing defined nodes of a network.")
@click.option('-e', '--edges', default=None, help="A TSV file containing defined edges of a network.")
@click.option('-l', '--labels', default=False, is_flag=True, help="Add relation type to edge labels if True.")
@click.option('-r', '--enrich', default=False, is_flag=True, help="Enrich the graph with RNA and DNA molecules.")
@click.argument('output_path')
def create(ppi: str, nodes: str, edges: str, output_path: str, labels: bool, enrich: bool):
    """Creates a graph image from a PPI file or node+edge lists."""
    analyzer = Analyzer(node_list=nodes, edge_list=edges, ppi_file=ppi, enrich=enrich)
    analyzer.generate_graph_image(graph_output_path=output_path, with_edge_labels=labels)


@main.command()
@click.option('-s', '--source', help="HGNC symbol for the starting/source node.")
@click.option('-t', '--target', help="HGNC symbol for the ending/target node.")
@click.argument('output_path')
@click.option('-p', '--ppi', default=None, help="A CSV file containing PPIs.")
@click.option('-n', '--nodes', default=None, help="A TSV file containing defined nodes of a network.")
@click.option('-e', '--edges', default=None, help="A TSV file containing defined edges of a network.")
@click.option('-v', '--verbose', default=False, is_flag=True, help="When used, will print the paths to STDOUT.")
@click.option('-r', '--enrich', default=False, is_flag=True, help="Enrich the graph with RNA and DNA molecules.")
def path(source: str, target: str, ppi: str, nodes: str, edges: str, output_path: str, verbose: bool, enrich: bool):
    """Generates a graph image highlighting specific paths between the given source and target."""
    path_finder = Analyzer(node_list=nodes, edge_list=edges, ppi_file=ppi, enrich=enrich)
    path_finder.shortest_paths(source, target, print_paths=verbose)
    path_finder.generate_graph_image(graph_output_path=output_path)


@main.command()
@click.option('-p', '--ppi', default=None, help="A CSV file containing PPIs.")
@click.option('-n', '--nodes', default=None, help="A TSV file containing defined nodes of a network.")
@click.option('-e', '--edges', default=None, help="A TSV file containing defined edges of a network.")
@click.option('-v', '--verbose', default=False, is_flag=True, help="Prints stats to STDOUT.")
@click.option('-r', '--enrich', default=False, is_flag=True, help="Enrich the graph with RNA and DNA molecules.")
@click.option('-o', '--output', default=None, help="File path to save summary stats.")
def stats(ppi: str, nodes: str, edges: str, output: str, verbose: bool, enrich: bool):
    """Generates node/edge lists from a PPI file."""
    sa = Statistics(node_list=nodes, edge_list=edges, ppi_file=ppi, enrich=enrich)
    sa.summary_statistics()

    if verbose:
        click.echo(sa.sum_stats)

    if output:
        sa.export_stats(output)


if __name__ == "__main__":
    main()

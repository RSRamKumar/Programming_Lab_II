from network import *

import click

# Start of CLI methods
@click.group()


def main():
    pass
@main.command()

@click.argument('ppi_file', type=click.Path(exists=True))
@click.argument('node_list')
@click.argument('edge_list')

def compile (ppi_file=None, node_list=None, edge_list=None) -> None:
    obj = Network(ppi_file)
    obj.compile_files(node_list,edge_list)



@main.command()
@click.option('-p', '--ppi_file', type=click.Path(exists=True), help="PPI file")
@click.option('-n', '--node_list', help= "Node file")
@click.option('-e', '--edge_list', help= "Edge file")
@click.option('--export',help='Name of the Output file')
@click.option('--print_table',help='Printing the Stat table')
def stats(ppi_file=None, node_list=None, edge_list=None , export=None,print_table=None) -> None:
    file_name,file_extension=os.path.splitext(export)

    if ppi_file:
        stat=Statistics(ppi_file)
        if print_table == True: print(repr(stat))
        if file_extension == '.json':
            stat.export_stats(export,JSON=True)

        if file_extension == '.csv':
            stat.export_stats(export,delimiter=',')

        if file_extension == '.tsv':
            stat.export_stats(export,delimiter='\t')
    if node_list and edge_list:
        stat=Statistics(node_list=node_list,edge_list=edge_list,)
        if print_table == "yes":print(repr(stat))
        if file_extension == '.json':
            stat.export_stats(export, JSON=True)

        if file_extension == '.csv':
            stat.export_stats(export, delimiter=',')

        if file_extension == '.tsv':
            stat.export_stats(export, delimiter='\t')




if __name__ == '__main__':
    main()


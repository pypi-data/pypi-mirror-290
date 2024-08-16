#!/usr/bin/env python
"""
File: fastq.py
Description: Instantiate a FASTA file object.
CreateDate: 2024/7/25
Author: xuwenlin
E-mail: wenlinxu.njfu@outlook.com
"""
from io import TextIOWrapper
from typing import Union
from collections import Counter
from os import getcwd
from os.path import abspath
from gzip import GzipFile
from random import randint, choice, choices
from click import echo, open_file
from pybioinformatic.sequence import Reads
from pybioinformatic.task_manager import TaskManager


def _stat_k_mer(seq_list: list) -> Counter:
    return Counter(seq_list)


class Fastq:
    def __init__(self, path: Union[str, TextIOWrapper]):
        """
        Initialize name, __open, and num_reads attributions.
        """
        if isinstance(path, str):
            self.name = abspath(path)
            if path.endswith('gz'):
                self.__open = GzipFile(path)
                self.num_reads = sum(1 for line in self.__open if str(line, 'utf8').startswith('@'))
                self.__open.seek(0)
            else:
                self.__open = open(path)
                self.num_reads = sum(1 for line in open(path) if line.startswith('@'))
        elif isinstance(path, TextIOWrapper):
            self.name = abspath(path.name)
            if path.name == '<stdin>':
                self.__open = open_file('-').readlines()
                self.num_reads = sum(1 for line in self.__open if line.startswith('@'))
            else:
                if path.name.endswith('gz'):
                    self.__open = GzipFile(path.name)
                    self.num_reads = sum(1 for line in self.__open if str(line, 'utf8').startswith('@'))
                    self.__open.seek(0)
                else:
                    self.__open = path
                    self.num_reads = sum(1 for line in self.__open if line.startswith('@'))
                    self.__open.seek(0)
        else:
            echo(f'\033[31mInvalid type: {type(path)}.\033[0m', err=True)
            exit()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            self.__open.close()
        except AttributeError:
            pass

# Basic method==========================================================================================================
    def __seek_zero(self):
        try:
            self.__open.seek(0)
        except AttributeError:
            pass

    def parse(self):
        while 1:
            record_id = self.__open.readline().strip()
            if not record_id:
                self.__seek_zero()
                break
            record_seq = self.__open.readline().strip()
            record_desc = self.__open.readline().strip()
            record_quality = self.__open.readline().strip()
            if self.name.endswith('gz'):
                record_id = str(record_id, 'utf8')
                record_seq = str(record_seq, 'utf8')
                record_desc = str(record_desc, 'utf8')
                record_quality = str(record_quality, 'utf8')
            yield Reads(seq_id=record_id, sequence=record_seq, desc=record_desc, quality=record_quality)

# K-mer method==========================================================================================================
    def get_k_mer(self, k: int = 21):
        """Get K-mer sequence for each sequence from fastq file."""
        for nucl in self.parse():
            yield from nucl.k_mer(k)

    def stat_k_mer(self, k: int = 21, output_path: str = getcwd()):
        """Count the frequency of each k-mer."""
        k_mer_list = (i for i in self.get_k_mer(k=k))
        seq_list = '\n'.join([i.seq for i in k_mer_list])
        with open(f'{output_path}/k-mer.seq', 'w') as o:
            o.write(seq_list)
        awk = r"awk '{print $1}'"
        cmd = f"sort {output_path}/k-mer.seq | uniq -c | {awk} | sort | uniq -c"
        tkm = TaskManager(num_processing=1)
        stdout = tkm.echo_and_exec_cmd(cmd=cmd, show_cmd=False).strip().split('\n')
        stdout = '\n'.join([i.strip().replace(' ', '\t') for i in stdout])
        return stdout

# Other method==========================================================================================================
    @staticmethod
    def generate_random_fastq(num_records: int,
                              record_length: Union[int, list, tuple] = 150,
                              base_bias: Union[float, list] = 1.0
                              ) -> str:
        """
        Generate a random FASTQ file.
        :param num_records: Number of records
        :param record_length: Length or length range of records
        :param base_bias: Base bias
        """
        seed = list('abcdefghijklmnopqrstuvwxyz0123456789'.upper())
        q_value = '!"#$%&\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}~'
        if isinstance(base_bias, float):
            base_bias = [base_bias for _ in range(5)]
        for _ in range(num_records):
            record_id = '@' + ''.join([choice(seed) for _ in range(10)])
            length = randint(min(record_length), max(record_length)) \
                if isinstance(record_length, (list, tuple)) else record_length
            record_seq = ''.join(choices(population="AGCTN", weights=base_bias, k=length))
            Q_value = ''.join(choices(population=q_value, k=length))
            yield f'{record_id}\n{record_seq}\n+\n{Q_value}'

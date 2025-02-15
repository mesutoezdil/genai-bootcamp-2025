import { useState, useEffect } from 'react';
import {
    Box,
    Typography,
    Table,
    TableBody,
    TableCell,
    TableContainer,
    TableHead,
    TableRow,
    Paper,
    Button
} from '@mui/material';
import axios from 'axios';

interface Word {
    id: number;
    simplified: string;
    pinyin: string;
    english: string;
}

const Words = () => {
    const [words, setWords] = useState<Word[]>([]);

    useEffect(() => {
        const fetchWords = async () => {
            try {
                const response = await axios.get('http://localhost:8000/words/');
                setWords(response.data);
            } catch (error) {
                console.error('Failed to fetch words:', error);
            }
        };

        fetchWords();
    }, []);

    return (
        <Box>
            <Typography variant="h4" gutterBottom>
                Words List
            </Typography>
            <TableContainer component={Paper}>
                <Table>
                    <TableHead>
                        <TableRow>
                            <TableCell>Chinese</TableCell>
                            <TableCell>Pinyin</TableCell>
                            <TableCell>English</TableCell>
                            <TableCell>Actions</TableCell>
                        </TableRow>
                    </TableHead>
                    <TableBody>
                        {words.map((word) => (
                            <TableRow key={word.id}>
                                <TableCell>{word.simplified}</TableCell>
                                <TableCell>{word.pinyin}</TableCell>
                                <TableCell>{word.english}</TableCell>
                                <TableCell>
                                    <Button variant="contained" size="small">
                                        Study
                                    </Button>
                                </TableCell>
                            </TableRow>
                        ))}
                    </TableBody>
                </Table>
            </TableContainer>
        </Box>
    );
};

export default Words; 
import { Box, Text } from "@chakra-ui/react";
import { useSelector } from "react-redux";
import useQrGenerator from "../../../hooks/useQrGenerator";

const QrGenerator = (props) => {
    const [canvasRef] = useQrGenerator(props.eventId);
    const userConnected = useSelector((state) => state.auth.userConnected);

    const downloadQrImage = () => {
        const image = canvasRef.current.toDataURL("image/png", 1.0).replace("image/png", "image/octet-stream");
        var link = document.createElement("a");
        link.download = "generated-qr-code.png";
        link.href = image;
        link.click();
    };

    return (
        <>
            <Box w="248px" h="248px">
                <canvas ref={canvasRef} />
            </Box>
            <Text ml="90px" mt="100px" fontFamily="PPTelegraf-Regular" fontSize="16" color="#847c7b">
                {userConnected?.name}
            </Text>
        </>
    );
};

export default QrGenerator;

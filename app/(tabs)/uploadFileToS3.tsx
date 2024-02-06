import AWS from 'aws-sdk';

AWS.config.update({
  accessKeyId: 'AKIATMD6HQGHGASZGVGK',
  secretAccessKey: '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',
  region: 'ap-southeast-1'
});

const s3 = new AWS.S3();

const uploadFileToS3 = async (bucketName, fileName, fileContent) => {
  const params = {
    Bucket: bucketName,
    Key: fileName,
    Body: fileContent,
    ContentType: 'image/jpeg', 
  };

  try {
    const data = await s3.upload(params).promise();
    console.log('File uploaded successfully', data);
    return data;
  } catch (err) {
    console.error('Error uploading to S3', err);
    throw err;
  }
};

export { uploadFileToS3 };